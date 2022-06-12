import time
from adapter.monkey import MonkeyAdapter
from rigControl import RigControl
import os
from utils import getAdapters
 

def main():
    rigControl = RigControl("/dev/cu.usbserial-1120")
    #rigControl.no_serial = True

    rigControl.init()

    rigControl.sendInitializeInInterfaceCommand()
    time.sleep(3)
    # rigControl.sendTurnToCommand(0, 2)

    # print("wating...")
    # time.sleep(10)

    monkeyAdapter = MonkeyAdapter(rigControl)
    monkeyAdapter.start()
    
if __name__ == '__main__':
    main()
    
