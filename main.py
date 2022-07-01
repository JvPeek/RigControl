from sqlite3 import adapt
import time
from adapter.monkey import MonkeyAdapter
from adapter.test import TestAdapter
#from adapter.warthunder import WTAdapter
from rigControl.rigControl import RigControl
import signal
import sys
import paho.mqtt.client as paho
import argparse




def main():
    parser = argparse.ArgumentParser(description='This is the bridge to receive data via UDP, parse it and send it to the brains of the rig.')
    parser.add_argument('-p', '--port', default="/dev/ttyUSB0",
                    help='Sets the port. Example: COM3. Default: /dev/ttyUSB0.')
    parser.add_argument('-i', '--interface', default="127.0.0.1",
                    help='Sets the interface to listen to. Default: 127.0.0.1')

    parser.add_argument('--offline', default=False, action="store_true",
                    help='Allows to run the app without brains attached.')
    args = parser.parse_args()

    if (args.offline):
        rigControl = RigControl(None)
        rigControl.no_serial = True
    else:
        rigControl = RigControl(args.port)

    rigControl.init()

    adapter = MonkeyAdapter(rigControl, args.interface)
    # adapter = WTAdapter(rigControl, "10.0.1.2")

    adapter.init()
    adapter.start()


    # broker="192.168.178.45"
    # port=1883
    #
    # client1= paho.Client("control1")                           #create client object
    # client1.connect(broker,port)                                 #establish connection
    # client1.publish("house/bulb1","on")                   #publish

    def signal_handler(sig, frame):
        nonlocal adapter
        print('Handling SIGINT (Ctrl+C)')
        adapter.stop()
        sys.exit()
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()
