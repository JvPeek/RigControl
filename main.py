from rigControl import RigControl
import time

def main():
    rigControl = RigControl()
    # rigControl.no_serial = True
    rigControl.init()

    rigControl.sendInitializeInInterfaceCommand()

    rigControl.sendTurnToCommand(60, 2)
    time.sleep(3)
    rigControl.sendTurnToCommand(20, 2)
    time.sleep(3)
    rigControl.sendTurnToCommand(0, 2)
    time.sleep(3)

    rigControl.runningReadSerial = False

if __name__ == '__main__':
    main()
    
