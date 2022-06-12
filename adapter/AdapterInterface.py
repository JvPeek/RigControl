import logging


class AdapterInterface(object):
    def __init__(self) -> None:
        self.log = logging.getLogger(f"Adapter.{self.__class__.__name__}")
        logging.basicConfig(level=logging.INFO)


        # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def init(self): pass
    def start(self): pass
    def stop(self): pass