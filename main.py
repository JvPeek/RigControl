from rigControl import RigControl



def main():
    RigControl.sendInitializeInInterfaceCommand()
    RigControl.sendTurnToCommand(60, 2)
    RigControl.sendTurnToCommand(21.7, 2)
    RigControl.sendTurnToCommand(0, 2)    

if __name__ == '__main__':
    main()
    
