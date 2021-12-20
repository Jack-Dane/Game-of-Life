
from abc import abstractmethod


class Frame:

    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        self.screen = None

    def setOffset(self, x, y):
        self.offsetX = x
        self.offsetY = y

    def addScreen(self, screen):
        self.screen = screen

    @abstractmethod
    def checkClicked(self, mousePosition):
        raise NotImplemented
