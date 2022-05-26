import time
from rigControl import RigControl
from tmAdapter import TMAdapter



def main():
    rigControl = RigControl()
    tmAdapter = TMAdapter()

    rigControl.init()

    rigControl.sendInitializeInInterfaceCommand()
    time.sleep(0.2)

    tmAdapter.attach()

if __name__ == '__main__':
    main()
    
