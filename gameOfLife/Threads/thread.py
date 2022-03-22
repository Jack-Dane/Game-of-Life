
from abc import ABC, abstractmethod
from threading import Thread, Event


class ThreadObject(Thread, ABC):

    def __init__(self):
        super(ThreadObject, self).__init__()
        self.stopThreadEvent = Event()

    @abstractmethod
    def stopThread(self):
        self.stopThreadEvent.set()

    def run(self):
        while not self.stopThreadEvent.is_set():
            self.loopExecution()

    @abstractmethod
    def loopExecution(self):
        raise NotImplementedError()
