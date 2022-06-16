
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

class WTAdapter:
    def __init__(self, rigControl: RigControl) -> None:
        self.last_stepped_time = 0
        self.update_interval = 10
        self.rigControl = rigControl

    def start(self): 
        x = threading.Thread(target=self.read_state)
        x.start() 

    def read_state(self):

        updateIntervalInMs = 50

        while True:
            timeStart = datetime.datetime.now()
            
            # sending get request and saving the response as response object
            r = requests.get(url = "http://192.168.178.24:8111/indicators")
            state = r.json()
        

            roll = state['aviahorizon_roll']

            roll = map(roll, -90, 90, -35, 35)


            print("would roll ", roll)

            self.rigControl.sendTurnToCommand(roll, 8)


            delta = datetime.datetime.now() - timeStart
            timeToSleepInMs = updateIntervalInMs - (delta.microseconds / 1000)
            if(timeToSleepInMs > 0):
                time.sleep(timeToSleepInMs / 1000)
            # time.sleep(0.010)
            

            


        
        

