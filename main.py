from rigControl import RigControl
from tmAdapter import TMAdapter

def main():
    tmAdapter = TMAdapter()


    RigControl.sendInitializeInInterfaceCommand()
    RigControl.sendTurnToCommand(60, 2)
    RigControl.sendTurnToCommand(20, 2)
    RigControl.sendTurnToCommand(0, 2)

    tmAdapter.attach()

if __name__ == '__main__':
    main()
    
