import socket
import struct
import math

import threading
from rigControl import RigControl


def offsetToFloat (buffer, offset, length):
    slice = buffer[offset:offset+length]
    return struct.unpack('<f', bytearray(slice))[0]


class MonkeyAdapter:
    def __init__(self, rigControl: RigControl) -> None:
        self.last_stepped_time = 0
        self.update_interval = 10
        self.rigControl = rigControl

    def start(self): 
        x = threading.Thread(target=self.read_state)
        x.start() 

    def read_state(self):
        localIP     = "0.0.0.0"
        localPort   = 12001
        bufferSize  = 1024

        lastAngle = 0

        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        UDPServerSocket.bind((localIP, localPort))
        print("UDP server up and listening")


        while(True):
            (message, _retAddress) = UDPServerSocket.recvfrom(bufferSize) 
            roll = math.degrees(offsetToFloat(message, 16, 4))
            print("roll", roll)
            dAngle = lastAngle - roll

            self.rigControl.sendTurnCommand()
            # self.rigControl.sendTurnToCommand(roll, 10)




# if __name__ == '__main__':
#     adapter = MonkeyAdapter()
#     adapter.start()



