import time
from monkeyAdapter import MonkeyAdapter
from rigControl import RigControl
from wtAdapter import WTAdapter


def main():
    rigControl = RigControl()
    # # rigControl.no_serial = True

    rigControl.init()

    rigControl.sendInitializeInInterfaceCommand()
    time.sleep(2)
    # rigControl.sendTurnToCommand(0, 2)

    # print("wating...")
    # time.sleep(10)

    monkeyAdapter = MonkeyAdapter(rigControl)
    monkeyAdapter.start()
    
if __name__ == '__main__':
    main()
    
