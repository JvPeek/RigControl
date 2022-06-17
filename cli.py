#!python3
import argparse
from adapter.adapters import getAdapters
from utils import getAvailablePorts
from rigControl.rigControl import RigControl
import signal
import sys


def argumentCommand(args):
    print(args.mainCommand)
    if(args.list == True):
        print(getAdapters().keys())

def runCommand(args):
    adapterClass = getAdapters()[args.adapter]

    rigControl = RigControl(serialport=args.port)
    #rigControl.no_serial = True
    adapter = adapterClass(rigControl)

    rigControl.init()
    adapter.init()

    adapter.start()

    def signal_handler(sig, frame):
        nonlocal adapter
        print('Handling SIGINT (Ctrl+C)')
        adapter.stop()
        sys.exit()
    signal.signal(signal.SIGINT, signal_handler)


def main():
    mainParser = argparse.ArgumentParser(description='RIG Controller -- Python Edition --')
    mainParser.add_argument('-p', type=str, choices=getAvailablePorts(), help="Serialport path", required=True, dest="port")

    mainSubparsers = mainParser.add_subparsers(help='sub-command help', required=True, dest="mainCommand")

    adapterParser = mainSubparsers.add_parser('adapter', help='Adapters help')
    adapterParser.add_argument('list', type=bool, help='bar help')
    
    runParser = mainSubparsers.add_parser('run', help='Adapters help')
    runParser.add_argument('-a', dest="adapter", choices=getAdapters().keys(), type=str, required=True, help='which adapter to use')

    args = mainParser.parse_args()

    commandDict = {
        "adapter": argumentCommand,
        "run": runCommand
    }
    commandDict[args.mainCommand](args)


    
if __name__ == '__main__':
    main()
    
