import time
from rigControl import RigControl



def main():
    RigControl.sendInitializeInInterfaceCommand()
    time.sleep(0.2)
    # RigControl.sendTurnToCommand(60, 2)
    # RigControl.sendTurnToCommand(21.7, 2)
    # RigControl.sendTurnToCommand(0, 2)    

    RigControl.sendTurnCommand(1)
    time.sleep(3)
    RigControl.sendTurnCommand(-1)
    time.sleep(3)
    RigControl.sendTurnCommand(0)
    

if __name__ == '__main__':
    main()
    
