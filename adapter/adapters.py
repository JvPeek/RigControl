
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