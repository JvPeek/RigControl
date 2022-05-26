from rigControl import RigControl
import time

def main():
    rigControl = RigControl()
    # rigControl.no_serial = True
    rigControl.sendInitializeInInterfaceCommand()

    rigControl.init()

    rigControl.sendTurnToCommand(60, 2)
    rigControl.sendTurnToCommand(20, 2)
    rigControl.sendTurnToCommand(0, 2)


    time.sleep(2)
    rigControl.runningReadSerial = False

if __name__ == '__main__':
    main()
    
