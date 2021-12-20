
from abc import ABC, abstractmethod


class View(ABC):

    def __init__(self):
        self.controller = None

    @abstractmethod
    def notify(self, subject):
        """
        Notify the view that the model has been updated
        :param subject: the updated model
        """
        pass

    def addController(self, controller):
        self.controller = controller
