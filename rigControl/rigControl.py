from functools import reduce
try:
    import serial
    import serial.tools.list_ports

except ImportError:
    print("[ERROR] No serial found")

import time
import threading
import logging
from datetime import datetime


class RigControl():
    COMMAND_INIT = 0x01
    COMMAND_TURN_TO = 0x10
    COMMAND_TURN = 0x11

    def __init__(self, serialport):
        self.log = logging.getLogger(f"RigControl")
        self.package_counter = 0x01
        self.no_serial = False
        self.runningReadSerial = True
        self.serial = serial.Serial(port=serialport, baudrate=115200)
        self.awaitingAck = list()

        self.logFileHandler = open("./reading.log", "a")

    def init(self):
        # if not self.no_serial: 
        self.serial.dtr = not(self.serial.dtr)
        time.sleep(0.1)
        self.serial.dtr = not(self.serial.dtr)

        x = threading.Thread(target=self.read_serial_function)
        x.start()
        self.log.info("started reading-thread. Will wait for 2sec")
        time.sleep(2)

    def read_serial_function(self):

        lastDebugMessage = None
        self.logFileHandler.write(f"\n\n\n############### NEW {datetime.now()} #############\n")
        print("READ: before loop")
        while self.runningReadSerial:
            cmd = ord(self.serial.read(size=1))
            # print("READ: in loop", cmd)

            id = ord(self.serial.read(size=1))
            size = ord(self.serial.read(size=1))
            buf = []
            i =0
            while i < size:
                buf.append(self.serial.read(size=1))
                i = i+1
            checksum = ord(self.serial.read(size=1))
            
            if cmd==0x74:
                # print ("helo")
                # self.logFileHandler.write("helo\n")
                pass
        
            elif cmd==0xfe:
                message = "[READ] debug: "
                for b in buf:
                    message += b.decode("ascii")
                if message != lastDebugMessage:
                    lastDebugMessage = message
                    #print(message)   
                    self.logFileHandler.write(message) 
            elif cmd==0xf0:
                print ("[READ] ACK: ", id, buf[0])
                self.receivedAckWithId(id)
                pass
            else:
                #print("[READ] cmd ", hex(cmd), ", id ", hex(id), ", size ", size, ", buf ", end='')
                self.logFileHandler.write(f"[READ] cmd {hex(cmd)}, id {hex(id)}, size {size}")

                for b in buf:
                    self.logFileHandler.write(f"   buf: {hex(ord(b))}")
                    #print(hex(ord(b)), end='')
                self.logFileHandler.write(f"   checksum: {hex(checksum)} \n")
                #print(", checksum ", hex(checksum))

        self.logFileHandler.close()
        self.log.info("[THREAD] stopped")



    def setPackageCounter(self, package_counter: int):
        if not isinstance(package_counter, int): 
            raise ValueError("package_counter has to be an integer")
        self.package_counter = package_counter

    def incrementPackageCounter(self):
        self.package_counter += 1
        if self.package_counter > 255: 
            self.package_counter = 1

    def sendCommand(self, cmdId: int, payload:bytes = None, debug: bool = False, waitForAck = True):
        command = bytearray(cmdId.to_bytes(1, byteorder='big'))
        if debug: print(" [sendCommand] Sending command", command)
        commandPackageCounter = self.package_counter
        command.append(commandPackageCounter)
        if debug: print(" [sendCommand] Appended package_counter", self.package_counter)
        self.incrementPackageCounter()
        if debug: print(" [sendCommand] next package_counter will be", self.package_counter)
        if payload != None:
            command.append(len(payload))
            command.extend(payload)
            if debug: print(" [sendCommand] Added payload of length", len(payload), "with value", payload)

        checksum = self.calculateChecksum(command)
        if debug: print(" [sendCommand] checksum", checksum, "for", command)
        command.append(checksum)
        ## print("would send: ", ", ".join("0x{:02x}".format(b)  for b in command))
        if not self.no_serial: 
            self.serial.write(command)
            if waitForAck: self.waitForAck(commandPackageCounter)
        return commandPackageCounter
    
    def sendInitializeInInterfaceCommand(self): 
        print("[RC] Sending initialize Interface")
        return self.sendCommand(RigControl.COMMAND_INIT, bytes(b'\x00\x00'), False, False)
            

    def sendTurnToCommand(self, targetDegree: float, speedInDegreePerSecond: int):
        if not isinstance(targetDegree, int) and not isinstance(targetDegree, float): 
            raise ValueError("targetDegree has to be an integer or float")
        if not isinstance(speedInDegreePerSecond, int): 
            raise ValueError("speedInDegreePerSecond has to be an integer")
        if targetDegree > 180 or targetDegree < -180:
            raise ValueError("targetDegree cannot be greater than 180 or less than -180 but is ", targetDegree)
        if speedInDegreePerSecond > 255 or speedInDegreePerSecond < 1:
            raise ValueError("speedInDegreePerSecond has to be between 1 and 255 but is ", speedInDegreePerSecond)
        print("")
        if targetDegree == 0:
             targetDegree = 0.2

        degreeValue = round(round(targetDegree, 1) * 10) # needs to be between 1800 or -1800
        degreeValueBytes = self.convertSignedValueIntoHighLowBytes(degreeValue)

        speedByte = speedInDegreePerSecond.to_bytes(1, byteorder='big')
        print(f"  [sendTurnToCommand] Sending degree Value {degreeValue}..." )
        self.logFileHandler.write(f"  [sendTurnToCommand] Sending degree Value {degreeValue}...\n" )
        id = self.sendCommand(RigControl.COMMAND_TURN_TO, degreeValueBytes + speedByte, False, False)
        print(f"  [sendTurnToCommand] ... with id {id}" )
        self.logFileHandler.write(f"  [sendTurnToCommand] ... with id {id}\n" )
        return id


    def sendTurnCommand(self, speedInDegreePerSecond: int): 
        speedInDegreePerSecondBytes = self.convertSignedValueIntoHighLowBytes(speedInDegreePerSecond)
        print(f"  [sendTurnCommand] Sending speed Value {speedInDegreePerSecondBytes}..." )
        id = self.sendCommand(RigControl.COMMAND_TURN, speedInDegreePerSecondBytes, True)
        print(f"  [sendTurnCommand] ... with id {id}" )
        return id

    def calculateChecksum(self, bytes: bytes):
        return reduce(lambda x,y: x^y, bytes, 0x00)

    def receivedAckWithId(self, id: int):
        print("---> receivedAckWithId", id)
        self.awaitingAck.append(id)

    def waitForAck(self, id: int):
        while not id in self.awaitingAck:
            time.sleep(0.001)
        self.awaitingAck.remove(id)
        print("--> Removed ACK", id)
        return

    def convertSignedValueIntoHighLowBytes(self, degreeValue: int):
        return bytes(((degreeValue >> 8) & 0xff, degreeValue & 0xff))