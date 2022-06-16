import time
import threading
from adapter.AdapterInterface import AdapterInterface
from rigControl.rigControl import RigControl

def getTimeAsMS():
    return int(round(time.time() * 1000))

class TestAdapter(AdapterInterface):
    def __init__(self, rigControl: RigControl) -> None:
        super().__init__()
        self.rigUpdateIntervalInMS = 100
        self.counterUpdateIntervalInSeconds = 0.5
        self.rigControl = rigControl
        self.stopThreads = False

        self.targetRigAngle = 0.0
        self.targetRigSpeed = 6

    def start(self): 
        readStateThread = threading.Thread(target=self.readState)
        readStateThread.start()

        print("started read state")

        updateRigThread = threading.Thread(target=self.updateRig)
        updateRigThread.start()

        print("started update rig")

    def readState(self):
        counter = 0
        modifier = 1

        while(not self.stopThreads):
            counter += modifier
            if counter >= 14 or counter <= -14:
                modifier *= -1
            roll = counter 

            time.sleep(self.counterUpdateIntervalInSeconds)
            self.targetRigAngle = roll
            print("updated targetRigAngle")

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
