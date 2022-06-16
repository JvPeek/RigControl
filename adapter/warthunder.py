
from os import times
import requests
import threading
import datetime
import time

from rigControl.rigControl import RigControl

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def getTimeAsMS():
    return int(round(time.time() * 1000))
class WTAdapter:
    def __init__(self, rigControl: RigControl) -> None:
        self.last_stepped_time = 0
        self.update_interval = 10
        self.rigUpdateIntervalInMS = 20
        self.rigControl = rigControl
        self.stopThreads = False

        self.targetRigAngle = 0.0
        self.targetRigSpeed = 13

    def start(self): 
        readStateThread = threading.Thread(target=self.readState)
        readStateThread.start()

        updateRigThread = threading.Thread(target=self.updateRig)
        updateRigThread.start()

    def readState(self):

        updateIntervalInMs = 50

        while True:
            timeStart = datetime.datetime.now()
            
            # sending get request and saving the response as response object
            r = requests.get(url = "http://192.168.178.24:8111/indicators")
            state = r.json()
        

            roll = state['aviahorizon_roll']

            roll = map(roll, -90, 90, -35, 35)

            self.targetRigAngle = roll
            # print("set roll ", roll)


            # delta = datetime.datetime.now() - timeStart
            # timeToSleepInMs = updateIntervalInMs - (delta.microseconds / 1000)
            # if(timeToSleepInMs > 0):
            #     time.sleep(timeToSleepInMs / 1000)
            # time.sleep(0.010)
            

    def updateRig(self):
        lastRigUpdateTime = getTimeAsMS()
        while(not self.stopThreads):
            newRigUpdateTime = getTimeAsMS()
            if(newRigUpdateTime < lastRigUpdateTime + self.rigUpdateIntervalInMS):
                continue
            lastRigUpdateTime = newRigUpdateTime
            print(f"rig angle {self.targetRigAngle}")
            self.rigControl.sendTurnToCommand(self.targetRigAngle, self.targetRigSpeed)


        
        

