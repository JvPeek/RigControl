import time
import requests
from adapter.AdapterInterface import AdapterInterface

from rigControl.rigControl import RigControl
from utils import mapRange
class WTAdapter(AdapterInterface):

    def __init__(self, rigControl: RigControl, ip: str = "0.0.0.0", port: int = 8111) -> None:
        super().__init__(rigControl)

        self.rigUpdateIntervalInMS = 1000
        self.targetRigSpeed = 13

        self.host = {
            "ip": ip,
            "port": port,
            "baseUrl": f"http://{ip}:{port}"
        }


    def __requestAndReturnJsonOrNone(self, url: str) -> requests.Response:
        try:
            return requests.get(url=url, timeout=0.2).json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return None

    def __requestState(self):
        return self.__requestAndReturnJsonOrNone(url = f"{self.host['baseUrl']}/state")

    def __requestIndicators(self):
        return self.__requestAndReturnJsonOrNone(url = f"{self.host['baseUrl']}/indicators")

    def __getRollFromIndicators(self) -> float:
        indicators = self.__requestIndicators()
        if indicators == None or (not indicators.has_key('aviahorizon_roll') or (not indicators["valid"])):
            return None

        roll = indicators['aviahorizon_roll']
        roll = mapRange(roll, -90, 90, -35, 35)

        return roll

    def __getRollFromState(self) -> float:
        state = self.__requestState()
        if state == None or (not state["valid"]):
            return None

        #TODO: Implement handling like in https://github.com/sjsone/RigControl/blob/ec37448d992dbb86f889da823273d208f2defd10/adapter/warthunder.py

        return 2.00
        

    def updateState(self):
        useIndicators = self.__getRollFromIndicators() != None
        print("updateing state")
        while(not self.stopThreads):  
            print("will update")
            angle = self.__getRollFromIndicators() if useIndicators else self.__getRollFromState()
            if(angle != None): 
                self.setTargetRigAngle(angle)
            time.sleep(0.7)
        print("finished updateState")

        