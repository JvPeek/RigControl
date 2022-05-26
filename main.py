from rigControl import RigControl

def main():
    rigControl = RigControl()
    rigControl.sendInitializeInInterfaceCommand()

    rigControl.init()

    rigControl.sendTurnToCommand(60, 2)
    rigControl.sendTurnToCommand(20, 2)
    rigControl.sendTurnToCommand(0, 2)

if __name__ == '__main__':
    main()
    
