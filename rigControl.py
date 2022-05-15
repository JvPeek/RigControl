from functools import reduce

class RigControlClass():
    COMMAND_INIT = 0x01
    COMMAND_TURN_TO = 0x10

    def __init__(self):
        ## maybe start package_counter at 0x01 instead of 0x00 ?
        self.package_counter = 0x00

        # self.serial = serial.Serial(...)

    def setPackageCounter(self, package_counter: int):
        if not isinstance(package_counter, int): 
            raise ValueError("package_counter has to be an integer")
        self.package_counter = package_counter
    
    def sendCommand(self, cmdId: int, payload:bytes = None, debug: bool = False):
        command = bytearray(cmdId.to_bytes(1, byteorder='big'))
        if debug: print(" [sendCommand] Sending command", command)
        command.append(self.package_counter)
        if debug: print(" [sendCommand] Appended package_counter", self.package_counter)
        self.package_counter += 1
        if debug: print(" [sendCommand] next package_counter will be", self.package_counter)
        if payload != None:
            command.append(len(payload))
            command.extend(payload)
            if debug: print(" [sendCommand] Added payload of length", len(payload), "with value", payload)

        checksum = reduce(lambda x,y: x^y, command, 0x00)
        if debug: print(" [sendCommand] checksum", checksum, "for", command)
        command.append(checksum)
        print("would send: ", ", ".join("0x{:02x}".format(b)  for b in command))
        # self.serial.send(command) ?
    
    def sendInitializeInInterfaceCommand(self): 
        self.sendCommand(RigControlClass.COMMAND_INIT, bytes(b'\x00\x00'))
            
    def sendTurnToCommand(self, targetDegree: int, speedInDegreePerSecond: int):
        if not isinstance(targetDegree, int): 
            raise ValueError("targetDegree has to be an integer")
        if not isinstance(speedInDegreePerSecond, int): 
            raise ValueError("speedInDegreePerSecond has to be an integer")
        if targetDegree > 180 or targetDegree < -180:
            raise ValueError("targetDegree cannot be greater than 180 or less than -180")
        if speedInDegreePerSecond > 255 or speedInDegreePerSecond < 1:
            raise ValueError("speedInDegreePerSecond has to be between 1 and 255")
        
        degreeValue = (targetDegree * 10) # needs to be between 1800 or -1800
        degreeValueBytes = self.convertDegreeValueIntoHighLowBytes(degreeValue)

        speedByte = speedInDegreePerSecond.to_bytes(1, byteorder='big')

        self.sendCommand(RigControlClass.COMMAND_TURN_TO, degreeValueBytes + speedByte)

    def convertDegreeValueIntoHighLowBytes(self, degreeValue: int):
        ## return known byte pair here if conversion does not work:
        # return bytes((0x69, 0x69))
        ## maybe bytes have to be swapped ? (compare with known values)
        return bytes(((degreeValue >> 8) & 0xff, degreeValue & 0xff))
    
RigControl = RigControlClass()