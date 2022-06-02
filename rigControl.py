from functools import reduce
try:
    import serial
except ImportError:
    print("[ERROR] No serial found")

import time
import threading


def ackReturnCodeToString(code):
    if ord(code) == 0x00:
        return "OK"
    elif ord(code) == 0x01:
        return "Parameter error"
    elif ord(code) == 0x02:
        return "Wrong checksum"
    elif ord(code) == 0x03:
        return "Not in interface mode"
    else:
        return "unknown status: " + hex(ord(code))

class RigControl():
    COMMAND_INIT = 0x01
    COMMAND_TURN_TO = 0x10
    COMMAND_TURN = 0x11

    def __init__(self):
        self.package_counter = 0x01
        self.no_serial = False
        self.arduino = None
        self.runningReadSerial = True
        

    def init(self):
        if not self.no_serial: 
            self.arduino = serial.Serial(port='/dev/cu.usbmodem11201', baudrate=115200)
        
            self.arduino.dtr = not(self.arduino.dtr)
            time.sleep(0.1)
            self.arduino.dtr = not(self.arduino.dtr)

        x = threading.Thread(target=self.read_serial_function)
        x.start()
        print ("[RC] Init complete. Will wait for 2sec")
        time.sleep(2)

    def read_serial_function(self):
        print ("[THREAD] starting to read from serial")
        while self.runningReadSerial and not self.no_serial:
            cmd = ord(self.arduino.read(size=1))
            id = ord(self.arduino.read(size=1))
            size = ord(self.arduino.read(size=1))
            buf = []
            for _ in range(size):
                buf.append(self.arduino.read(size=1))
            checksum = ord(self.arduino.read(size=1))

            if cmd == 0x01:
                print ("[READ] init: Status="+ackReturnCodeToString(buf[0])+" V="+hex(ord(buf[1]))+"."+hex(ord(buf[2])), end='')
                print (" SN="+hex(ord(buf[3]))+" "+hex(ord(buf[4]))+" "+hex(ord(buf[5]))+" "+hex(ord(buf[6])))
            elif cmd==0x74:
                #print ("[READ] helo")
                pass
            elif cmd==0xfe:
                print ("[READ] debug: ", end='')
                for b in buf:
                    print(b.decode("ascii"), end='')
                print("")    
            elif cmd==0xf011:
                print ("[READ] ACK: ", ackReturnCodeToString(buf[0]))
            else:
                print("[READ] cmd ", hex(cmd), ", id ", hex(id), ", size ", size, ", buf ", end='')
                for b in buf:
                    print(hex(ord(b)), end='')
                print(", checksum ", hex(checksum))

        print ("[THREAD] stopped")



    def setPackageCounter(self, package_counter: int):
        if not isinstance(package_counter, int): 
            raise ValueError("package_counter has to be an integer")
        self.package_counter = package_counter

    def incrementPackageCounter(self):
        self.package_counter += 1
        if self.package_counter > 255: 
            self.package_counter = 1

    def sendCommand(self, cmdId: int, payload:bytes = None, debug: bool = False):
        command = bytearray(cmdId.to_bytes(1, byteorder='big'))
        if debug: print(" [sendCommand] Sending command", command)
        command.append(self.package_counter)
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
        if debug: print("[RC] would send: ", ", ".join("0x{:02x}".format(b)  for b in command))
        if not self.no_serial: 
            self.arduino.write(command)
    
    def sendInitializeInInterfaceCommand(self): 
        print("[RC] Sending initialize Interface")
        self.sendCommand(RigControl.COMMAND_INIT, bytes(b'\x00\x00'))
            

    def sendTurnToCommand(self, targetDegree: float, speedInDegreePerSecond: int):
        if not isinstance(targetDegree, int) and not isinstance(targetDegree, float): 
            raise ValueError("targetDegree has to be an integer or float")
        if not isinstance(speedInDegreePerSecond, int): 
            raise ValueError("speedInDegreePerSecond has to be an integer")
        if targetDegree > 180 or targetDegree < -180:
            raise ValueError("targetDegree cannot be greater than 180 or less than -180 but is ", targetDegree)
        if speedInDegreePerSecond > 255 or speedInDegreePerSecond < 1:
            raise ValueError("speedInDegreePerSecond has to be between 1 and 255 but is ", speedInDegreePerSecond)
        
        degreeValue = round(round(targetDegree, 1) * 10) # needs to be between 1800 or -1800
        #print("  [sendTurnToCommand] Degree Value", degreeValue)
        degreeValueBytes = self.convertSignedValueIntoHighLowBytes(degreeValue)

        speedByte = speedInDegreePerSecond.to_bytes(1, byteorder='big')

        self.sendCommand(RigControl.COMMAND_TURN_TO, degreeValueBytes + speedByte)

    def sendTurnCommand(self, speedInDegreePerSecond: int): 
        speedInDegreePerSecondBytes = self.convertSignedValueIntoHighLowBytes(speedInDegreePerSecond)
        self.sendCommand(RigControl.COMMAND_TURN, speedInDegreePerSecondBytes)

    def calculateChecksum(self, bytes):
        return reduce(lambda x,y: x^y, bytes, 0x00)

    def convertSignedValueIntoHighLowBytes(self, degreeValue: int):
        ## return known byte pair here if conversion does not work:
        # return bytes((0x69, 0x69))
        ## maybe bytes have to be swapped ? (compare with known values)
        return bytes(((degreeValue >> 8) & 0xff, degreeValue & 0xff))