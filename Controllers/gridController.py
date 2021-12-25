
import time
from threading import Thread, Event

from Observers.observer import Model


class GridController(Thread, Model):

    def __init__(self, grid):
        Thread.__init__(self)
        Model.__init__(self)
        self.pausedEvent = Event()
        self.pausedEvent.set()
        self.stoppedEvent = Event()
        self.continueEvent = Event()
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
            self.notifyObservers()
            self.waitForContinue()
            self.pausedEvent.clear()
        if self.stoppedEvent.is_set():
            self.grid.clearGrid(update=True)
            self.waitForContinue()
            self.stoppedEvent.clear()
        self.notifyObservers()

    def clickGridItem(self, x, y):
        self.grid.checkGridItem(x, y)

    def waitForContinue(self):
        self.continueEvent.wait()
        self.continueEvent.clear()

    def startContinueGrid(self):
        self.continueEvent.set()

    def stopPauseGrid(self):
        if self.pausedEvent.is_set():
            self.stoppedEvent.set()
            self.continueEvent.set()
        else:
            self.pausedEvent.set()

    def gridItemSelected(self, x, y):
        self.grid.click(x, y)

    @property
    def state(self):
        """
        :return: False if paused else True
        """
        return False if self.pausedEvent.is_set() else True

    def getData(self):
        return self.state
