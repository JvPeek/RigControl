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
        self.rigUpdateIntervalInMS = 100
        self.rigControl = rigControl
        self.stopReadStateThread = False

    def start(self): 
        readStateThread = threading.Thread(target=self.read_state)
        readStateThread.start() 

    def read_state(self):
        serverIp = "0.0.0.0"
        serverPort = 12001
        receiveBufferSize = 1024

        serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        serverSocket.bind((serverIp, serverPort))
        self.log.info(f'UDP server up and listening on {serverIp}:{serverPort}')

        lastRigUpdateTime = getTimeAsMS()

        while(not self.stopReadStateThread):
            (message, _retAddress) = serverSocket.recvfrom(receiveBufferSize) 
            newRigUpdateTime = getTimeAsMS()
            if(newRigUpdateTime < lastRigUpdateTime + self.rigUpdateIntervalInMS):
                continue
            rollInRadians = offsetToFloat(message, 16, 4)
            roll = math.degrees(rollInRadians)
            print("roll", roll, rollInRadians, newRigUpdateTime)

            
                # pass
            self.rigControl.sendTurnToCommand(roll, 4)

    def stop(self):
        self.stopReadStateThread = True
