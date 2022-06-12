import logging


class AdapterInterface(object):
    def __init__(self) -> None:
        self.log = logging.getLogger(f"Adapter.{self.__class__.__name__}")
        logging.basicConfig(level=logging.INFO)
        self.rigDegree = 0.0

    def init(self): pass
    def start(self): pass
    def stop(self): pass

    def getRigDegree(self):
        return self.rigDegree
