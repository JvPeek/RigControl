import time
from rigControl import RigControl
from tmAdapter import TMAdapter


def main():
    rigControl = RigControl()
    # rigControl.no_serial = True

    rigControl.init()

    rigControl.sendInitializeInInterfaceCommand()
    time.sleep(2)
    rigControl.sendTurnToCommand(0, 2)

    print("wating...")
    time.sleep(10)
    tmAdapter = TMAdapter(rigControl)

    tmAdapter.attach()
if __name__ == '__main__':
    main()
    
