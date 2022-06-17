from sqlite3 import adapt
import time
from adapter.monkey import MonkeyAdapter
from adapter.test import TestAdapter
from adapter.warthunder import WTAdapter
from rigControl.rigControl import RigControl
import signal
import sys


def main():
    rigControl = RigControl("/dev/cu.usbmodem1201")
    #rigControl.no_serial = True

    rigControl.init()
    
    adapter = MonkeyAdapter(rigControl)
    # adapter = WTAdapter(rigControl, "10.0.1.2")

    adapter.init()
    adapter.start()


    def signal_handler(sig, frame):
        nonlocal adapter
        print('Handling SIGINT (Ctrl+C)')
        adapter.stop()
        sys.exit()



    signal.signal(signal.SIGINT, signal_handler)

    
if __name__ == '__main__':
    main()
    
