import time
from adapter.monkey import MonkeyAdapter
from rigControl.rigControl import RigControl
import os
from utils import getAdapters
 

def main():
    rigControl = RigControl("/dev/cu.usbmodem11201")
    #rigControl.no_serial = True

    rigControl.init()

    rigControl.sendInitializeInInterfaceCommand()
    time.sleep(3)
    # rigControl.sendTurnToCommand(0, 2)

    # print("wating...")
    # time.sleep(10)

    # monkeyAdapter = MonkeyAdapter(rigControl)
    # monkeyAdapter.start()

    while True:
        for i in range(10):
            rigControl.sendTurnToCommand(i * 1, 5)
            time.sleep(0.1)
    
if __name__ == '__main__':
    main()
    
