import serial.tools.list_ports

from adapter.AdapterInterface import AdapterInterface
from adapter.trackmania import TMAdapter
from adapter.warthunder import WTAdapter
from adapter.monkey import MonkeyAdapter

def getAdapters() -> dict[str, AdapterInterface]:
    return {
        "monkey": MonkeyAdapter,
        "trackmania": TMAdapter,
        "warthunder": WTAdapter
    }

def getAvailablePorts():
    ports = serial.tools.list_ports.comports()

    return list(map( lambda thing: thing.device , sorted(ports)))
