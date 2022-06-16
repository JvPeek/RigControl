from cgi import test
import time
from adapter.monkey import MonkeyAdapter
from adapter.test import TestAdapter
from rigControl.rigControl import RigControl
import os
from utils import getAdapters
 

def main():
    rigControl = RigControl("/dev/cu.usbserial-130")
    #rigControl.no_serial = True

    rigControl.init()

    rigControl.sendInitializeInInterfaceCommand()
    time.sleep(10)
    # rigControl.sendTurnCommand(0)

    # time.sleep(15)

    # print("wating...")
    # time.sleep(10)

    for i in range(2, 15, 1): 
    # for i in map(lambda x: x/10.0, range(10, 150, 5)):
        print("TurnTo: ", i)
        rigControl.sendTurnToCommand(i, 4)
        time.sleep(2)

    # for i in range(0, 10, 2): 
    #     print("TurnTo: ", i)
    #     rigControl.sendTurnCommand(i)
    #     time.sleep(0.4)
    # rigControl.sendTurnCommand(0)

    # print("Will start")
    # runAdapter(rigControl)
    # runTest(rigControl)
    #runTestAdapter(rigControl)

def runAdapter(rigControl): 
    monkeyAdapter = MonkeyAdapter(rigControl)
    monkeyAdapter.start()

def runTest(rigControl):
    while True:
        for i in range(10):
            rigControl.sendTurnToCommand(i * 1, 5)
            time.sleep(0.1)

def runTestAdapter(rigControl):
    testAdapter = TestAdapter(rigControl)
    testAdapter.start()
    
if __name__ == '__main__':
    main()
    
