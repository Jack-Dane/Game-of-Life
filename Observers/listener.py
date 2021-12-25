
from abc import abstractmethod


class Listener:

    @abstractmethod
    def notify(self, subject):
        """
        Notify the view that the model has been updated
        :param subject: the updated model
        """
        raise NotImplementedError()
