
from abc import ABC


class View(ABC):

    def __init__(self):
        self.controller = None

    def addController(self, controller):
        self.controller = controller
