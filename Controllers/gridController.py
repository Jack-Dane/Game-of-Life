
import time
from threading import Thread


class GridController(Thread):

    def __init__(self, grid):
        super(GridController, self).__init__()
        self.paused = False
        self.grid = grid

    def run(self):
        super(GridController, self).run()
        self.startGrid()

    def startGrid(self):
        """
        Start the process on a thread
        """
        while not self.grid.same:
            if not self.paused:
                self.grid.update()
            time.sleep(.1)

    def stopGrid(self):
        pass

    def continueGrid(self):
        self.paused = False

    def pauseGrid(self):
        self.paused = True
