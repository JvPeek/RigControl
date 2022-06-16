
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

        updateIntervalInMs = 70

        rigState = {
            "angle": 0,
            "rigAngle": 0,
            "planeAngle": 0
        }


        while True:
            timeStart = datetime.datetime.now()
            
            # sending get request and saving the response as response object
            r = requests.get(url = "http://192.168.178.24:8111/state")

            state = r.json() 
        
            if not state["valid"]: 
                return

            wx = state['Wx, deg/s']

            wxDt = wx * (updateIntervalInMs / 1000)

            rigState["planeAngle"] = rigState["planeAngle"] % 360
            if (rigState["planeAngle"] < -180):
                 rigState["planeAngle"] = 180
            if (rigState["planeAngle"] > 180):
                 rigState["planeAngle"] = -180

            if (wxDt > 0.02 or wxDt < -0.02): 
                rigState["planeAngle"] += wxDt    
            else:
                rigState["planeAngle"] += (rigState["planeAngle"] * -1 / 50)
                if (rigState["planeAngle"] > -0.5 and rigState["planeAngle"] < 0.5):
                    rigState["planeAngle"] = 0
                
            rigState['angle'] = rigState["planeAngle"]


            if (rigState['angle'] > 90):
                rigState['angle'] = 90 - (rigState['angle'] - 90)
            
            if (rigState['angle'] < -90):
                rigState['angle'] = -90 - (rigState['angle'] + 90)
            

            rigState['angle'] = round(rigState['angle'] * 10) / 10


            # rigState['rigAngle'] = map(rigState['angle'], -90, 90, -22, 22)
            rigState['rigAngle'] = rigState['angle']


            print("wx", state['Wx, deg/s'], " wxdt", wxDt , "rig angle", rigState['rigAngle'])

            self.rigControl.sendTurnToCommand(rigState['rigAngle'], 8)


            delta = datetime.datetime.now() - timeStart
            timeToSleepInMs = updateIntervalInMs - (delta.microseconds / 1000)
            if(timeToSleepInMs > 0):
                time.sleep(timeToSleepInMs / 1000)
            # time.sleep(0.010)
            

            


        
        

