import socket
import struct
import math
import time
import threading
from rigControl import RigControl


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

class MonkeyAdapter:
    def __init__(self, rigControl: RigControl) -> None:
        self.last_stepped_time = 0
        self.update_interval = 10
        self.rigControl = rigControl

    def start(self): 
        x = threading.Thread(target=self.read_state)
        x.start() 

    def read_state(self):
        localIP = "0.0.0.0"
        localPort = 12001
        bufferSize = 1024

        rigUpdateIntervalInMS = 200

        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        UDPServerSocket.bind((localIP, localPort))
        print("UDP server up and listening")

        lastRigUpdateTime = getTimeAsMS()

        while(True):
            (message, _retAddress) = UDPServerSocket.recvfrom(bufferSize) 
            roll = math.degrees(offsetToFloat(message, 16, 4))
            print("roll", roll)

            newRigUpdateTime = getTimeAsMS()
            if(newRigUpdateTime < lastRigUpdateTime + rigUpdateIntervalInMS):
                continue
            self.rigControl.sendTurnToCommand(roll, 12)
            lastRigUpdateTime = newRigUpdateTime
