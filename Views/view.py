
from abc import ABC, abstractmethod


class View(ABC):

    @abstractmethod
    def notify(self, subject):
        """
        Notify the view that the model has been updated
        :param subject: the updated model
        """
        pass
