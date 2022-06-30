import socket
import struct
import math
from adapter.AdapterInterface import AdapterInterface
from rigControl.rigControl import RigControl
from utils import mapRange


def offsetToFloat (buffer, offset, length):
    slice = buffer[offset:offset+length]
    return struct.unpack('<f', bytearray(slice))[0]

class MonkeyAdapter(AdapterInterface):
    def __init__(self, rigControl: RigControl, ip: str = "0.0.0.0", port:int = 12001) -> None:
        super().__init__(rigControl)
        self.rigUpdateIntervalInMS = 70

        self.targetRigSpeed = 8

        self.host = {
            "ip": ip,
            "port": port
        }

    def updateState(self):
        serverIp = self.host['ip']
        serverPort = self.host['port']
        receiveBufferSize = 1024

        serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        serverSocket.bind((serverIp, serverPort))
        self.log.info(f'UDP server up and listening on {serverIp}:{serverPort}')

        while(not self.stopThreads):
            (message, _retAddress) = serverSocket.recvfrom(receiveBufferSize) 
            
            rollInRadians = offsetToFloat(message, 16, 4)
            roll = math.degrees(rollInRadians)
            roll = mapRange(roll, -90, 90, -35, 35)
            #self.log.info(f"\t\t\tGot update from SpaceMonkey {roll} {rollInRadians}")
            self.setTargetRigAngle(roll)
