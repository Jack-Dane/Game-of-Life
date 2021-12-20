
import time
from threading import Thread, Event


class GridController(Thread):

    def __init__(self, grid):
        super(GridController, self).__init__()
        self.pausedEvent = Event()
        self.pausedEvent.set()
        self.stoppedEvent = Event()
        self.continueEvent = Event()
        self.stopped = False
        self.paused = True
        self.grid = grid

    def run(self):
        super(GridController, self).run()
        self.startGrid()

    def startGrid(self):
        """
        Start the process on a thread
        """
        self.grid.start()
        while True:
            self.checkForEvents()
            self.grid.update()
            time.sleep(.1)

    def checkForEvents(self):
        if self.pausedEvent.is_set():
            self.pausedEvent.clear()
            self.waitForContinue()
        if self.stoppedEvent.is_set():
            self.stoppedEvent.clear()
            self.grid.clearGrid(update=True)
            self.waitForContinue()

    def clickGridItem(self, x, y):
        self.grid.checkGridItem(x, y)

    def waitForContinue(self):
        self.continueEvent.wait()
        self.continueEvent.clear()

    def stopGrid(self):
        self.stoppedEvent.set()

    def continueGrid(self):
        self.continueEvent.set()

    def pauseGrid(self):
        self.pausedEvent.set()

    def gridItemSelected(self, x, y):
        self.grid.click(x, y)
