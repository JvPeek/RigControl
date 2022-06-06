
from os import times
import requests
import threading
import datetime
import time

from rigControl import RigControl

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
            r = requests.get(url = "http://10.0.1.46:8111/state")

            state = r.json() 
            
            if not state["valid"]: 
                return
            print( state['Wx, deg/s'])


            self.rigControl.sendTurnCommand(state['Wx, deg/s'])



            delta = datetime.datetime.now() - timeStart
            timeToSleepInMs = updateIntervalInMs - (delta.microseconds / 1000)
            if(timeToSleepInMs > 0):
                time.sleep(timeToSleepInMs / 1000)
            # time.sleep(0.010)
            

            


        
        

