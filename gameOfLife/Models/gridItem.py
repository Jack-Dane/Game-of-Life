
from gameOfLife.Observers.subject import Subject


class GridItem(Subject):

    def __init__(self, x, y):
        super(GridItem, self).__init__()
        self.x = x
        self.y = y
        self.active = False
        self.nextIteration = False

    def __str__(self):
        return "1" if self.active else "0"

    @property
    def color(self):
        """
        What color the gridItem should be
        :return: A tuple RGB value
        """
        if self.active:
            return 170, 170, 170
        return 0, 0, 0

    def markActive(self):
        self.active = True

    def markInactive(self, nextIteration=False):
        """
        Mark the gridItem as inactive
        :param nextIteration: If True will set nextIteration to inactive as well
        """
        self.active = False
        if nextIteration:
            self.nextIteration = False

    def toggleActive(self):
        self.active = not self.active

    def getData(self):
        return self.active

    def shouldChange(self, totalSurrounding):
        """
        Based on the surrounding number of acitve tiles should this tile
        1. Die if it is alive
        2. Reproduce if it is dead
        3. Stay alive
        :param totalSurrounding: Number of active surrounding tiles
        """
        if self.active:
            self.shouldDie(totalSurrounding)
        else:
            self.shouldReproduce(totalSurrounding)

    def shouldDie(self, totalSurrounding):
        """
         This function is called on an active gridItem to determine if it should die
         :param totalSurrounding: Number of active surrounding tiles
         """
        if totalSurrounding not in range(2, 4):
            self.nextIteration = False
        else:
            self.nextIteration = True

    def shouldReproduce(self, totalSurrounding):
        """
        This function is called on an inactive gridItem to determine if it should come
        to life in the next iteration
        :param totalSurrounding: Number of active surrounding tiles
        """
        if totalSurrounding == 3:
            self.nextIteration = True
        else:
            self.nextIteration = False

    def update(self):
        """
        Make the nextIteration value equal to the current active value
        """
        self.active = self.nextIteration

    def checkSame(self):
        return self.active == self.nextIteration
