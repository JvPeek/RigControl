import socket
import struct
import math
import time
import threading
from adapter.AdapterInterface import AdapterInterface
from rigControl.rigControl import RigControl


def offsetToFloat (buffer, offset, length):
    slice = buffer[offset:offset+length]
    return struct.unpack('<f', bytearray(slice))[0]

def getTimeAsMS():
    return int(round(time.time() * 1000))

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class MonkeyAdapter(AdapterInterface):
    def __init__(self, rigControl: RigControl) -> None:
        super().__init__()
        self.rigUpdateIntervalInMS = 70
        self.rigControl = rigControl
        self.stopThreads = False

        self.targetRigAngle = 0.0
        self.targetRigSpeed = 8

    def start(self): 
        readStateThread = threading.Thread(target=self.readState)
        readStateThread.start()

        updateRigThread = threading.Thread(target=self.updateRig)
        updateRigThread.start()

    def readState(self):
        serverIp = "0.0.0.0"
        serverPort = 12001
        receiveBufferSize = 1024

        serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        serverSocket.bind((serverIp, serverPort))
        self.log.info(f'UDP server up and listening on {serverIp}:{serverPort}')

        while(not self.stopThreads):
            (message, _retAddress) = serverSocket.recvfrom(receiveBufferSize) 
            
            rollInRadians = offsetToFloat(message, 16, 4)
            roll = math.degrees(rollInRadians)
            roll = map(roll, -90, 90, -10, 10)
            # self.log.info(f"\t\t\tGot update from SpaceMonkey {roll} {rollInRadians}")
            self.targetRigAngle = roll

    def updateRig(self):
        lastRigUpdateTime = getTimeAsMS()
        while(not self.stopThreads):
            newRigUpdateTime = getTimeAsMS()
            if(newRigUpdateTime < lastRigUpdateTime + self.rigUpdateIntervalInMS):
                continue
            lastRigUpdateTime = newRigUpdateTime

            self.rigControl.sendTurnToCommand(self.targetRigAngle, self.targetRigSpeed)

    def stop(self):
        self.stopThreads = True
