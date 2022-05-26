from functools import reduce
import serial
import time
import threading


class RigControl():
    COMMAND_INIT = 0x01
    COMMAND_TURN_TO = 0x10
    COMMAND_TURN = 0x11

    def __init__(self):
        ## maybe start package_counter at 0x01 instead of 0x00 ?
        self.package_counter = 0x01
        self.arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
        
        self.arduino.dtr = not(self.arduino.dtr)
        time.sleep(0.1)
        self.arduino.dtr = not(self.arduino.dtr)

        self.runningReadSerial = True

        # self.serial = serial.Serial(...)

    def init(self):
        x = threading.Thread(target=self.read_serial_function)
        x.start()
        print ("started reading-thread. Will wait for 2sec")
        time.sleep(2)

    def read_serial_function(self):
        while self.runningReadSerial:
            cmd = ord(self.arduino.read(size=1))
            id = ord(self.arduino.read(size=1))
            size = ord(self.arduino.read(size=1))
            buf = []
            i =0
            while i < size:
                buf.append(self.arduino.read(size=1))
                i = i+1
            checksum = ord(self.arduino.read(size=1))

            if cmd==0x74:
                print ("helo")
            elif cmd==0xfe:
                print ("debug: ", end='')
                for b in buf:
                    print(b.decode("ascii"), end='')
                print("")    
            elif cmd==0xf0:
                print ("ACK: ", end='')
                if ord(buf[0]) == 0x00:
                    print ("OK")
                elif ord(buf[0]) == 0x01:
                    print ("Parameter error")
                elif ord(buf[0]) == 0x02:
                    print ("Wrong checksum")
                elif ord(buf[0]) == 0x03:
                    print ("Not in interface mode")
                else:
                    print ("unknown status", end='')
                    print (hex(ord(buf[0])))
            else:
                print("cmd ", end='')
                print(hex(cmd), end='')
                print(", id ", end='')
                print(hex(id), end='')
                print(", size ", end='')
                print(size, end='')
                print(", buf ", end='')
                for b in buf:
                    print(hex(ord(b)), end='')
                print(", checksum ", end='')
                print(hex(checksum), end='')
                print("")    



    def setPackageCounter(self, package_counter: int):
        if not isinstance(package_counter, int): 
            raise ValueError("package_counter has to be an integer")
        self.package_counter = package_counter

    def incrementPackageCounter(self):
        self.package_counter += 1
        if self.package_counter > 255: 
            self.package_counter = 0

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

        checksum = reduce(lambda x,y: x^y, command, 0x00)
        if debug: print(" [sendCommand] checksum", checksum, "for", command)
        command.append(checksum)
        print("would send: ", ", ".join("0x{:02x}".format(b)  for b in command))
        self.arduino.write(command)
    
    def sendInitializeInInterfaceCommand(self): 
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
        print("Degree Value", degreeValue)
        degreeValueBytes = self.convertDegreeValueIntoHighLowBytes(degreeValue)

        speedByte = speedInDegreePerSecond.to_bytes(1, byteorder='big')

        self.sendCommand(RigControl.COMMAND_TURN_TO, degreeValueBytes + speedByte)

    def sendTurnCommand(self, speedInDegreePerSecond: int): 
        speedInDegreePerSecondBytes = self.convertDegreeValueIntoHighLowBytes(speedInDegreePerSecond)
        self.sendCommand(RigControl.COMMAND_TURN, speedInDegreePerSecondBytes)

    def convertDegreeValueIntoHighLowBytes(self, degreeValue: int):
        ## return known byte pair here if conversion does not work:
        # return bytes((0x69, 0x69))
        ## maybe bytes have to be swapped ? (compare with known values)
        return bytes(((degreeValue >> 8) & 0xff, degreeValue & 0xff))