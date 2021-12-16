
import random

from Models.model import Model


class GridItem(Model):

    def __init__(self, x, y):
        super(GridItem, self).__init__()
        self.x = x
        self.y = y
        self.active = True if random.randint(0, 5) == 1 else False
        self.nextIteration = False

    def __str__(self):
        return "1" if self.active else "0"

    @property
    def color(self):
        if self.active:
            return 170, 170, 170
        return 0, 0, 0

    def markActive(self):
        self.active = True

    def markInactive(self):
        self.active = False

    def toggleActive(self):
        self.active = not self.active

    def getData(self):
        return self.active

    def shouldChange(self, totalSurrounding):
        if self.active:
            self.shouldDie(totalSurrounding)
        else:
            self.shouldReproduce(totalSurrounding)

    def shouldDie(self, totalSurrounding):
        if totalSurrounding not in range(2, 4):
            self.nextIteration = False

    def shouldReproduce(self, totalSurrounding):
        if totalSurrounding == 3:
            self.nextIteration = True

    def update(self):
        self.active = self.nextIteration
