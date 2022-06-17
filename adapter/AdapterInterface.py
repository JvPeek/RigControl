import logging
import threading
import time
from rigControl.rigControl import RigControl

from utils import getTimeAsMS


class AdapterInterface(object):
    def __init__(self, rigControl: RigControl) -> None:
        self.log = logging.getLogger(f"Adapter.{self.__class__.__name__}")
        logging.basicConfig(level=logging.INFO)

        self.rigControl = rigControl

        self.updateRigThread = None
        self.updateStateThread = None
        self.rigUpdateIntervalInMS = 20

        self.targetRigAngle = 0.0
        self.targetRigSpeed = 6

        self.stopThreads = False

    def init(self):
        self.log.info("Sending initalize interface...")
        self.rigControl.sendInitializeInInterfaceCommand()
        self.log.info("...will wait for 10 seconds")
        time.sleep(10)

    def start(self): 
        self.__startUpdateRigThread()
        self.__startUpdateStateThread()

    def stop(self):
        self.stopThreads = True 
        #FIXME: cannot join if thread hangs
        # self.updateRigThread.join()
        # self.updateStateThread.join()

    def __startUpdateRigThread(self):
        self.updateRigThread = threading.Thread(target=self.updateRig)
        self.updateRigThread.start()

    def __startUpdateStateThread(self):
        self.updateStateThread = threading.Thread(target=self.updateState)
        self.updateStateThread.start()

    def updateRig(self):
        lastRigUpdateTime = getTimeAsMS()
        while(not self.stopThreads):
            newRigUpdateTime = getTimeAsMS()
            if(newRigUpdateTime < lastRigUpdateTime + self.rigUpdateIntervalInMS):
                continue
            lastRigUpdateTime = newRigUpdateTime
            #print(f"rig angle {self.targetRigAngle}")
            self.rigControl.sendTurnToCommand(self.targetRigAngle, self.targetRigSpeed)

    def setTargetRigAngle(self, angle: float):
        self.targetRigAngle = angle

    def updateState(self):
        while(not self.stopThreads):
            print(f"[{self.__class__.__name__}] method updateState not implemented...")
            time.sleep(5)
