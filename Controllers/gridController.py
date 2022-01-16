
import time
from threading import Event

from Observers.subject import Subject
from Threads.thread import ThreadObject


class GridController(ThreadObject, Subject):

    def __init__(self, grid):
        ThreadObject.__init__(self)
        Subject.__init__(self)
        self.stopThreadEvent = Event()
        self.pausedEvent = Event()
        self.stoppedEvent = Event()
        self.stoppedEvent.set()
        self.continueEvent = Event()
        self.grid = grid

    def run(self):
        self.grid.start()
        ThreadObject.run(self)

    def loopExecution(self):
        """
        Start the process on a thread
        """
        self.checkForEvents()
        self.grid.update()
        time.sleep(.1)

    def checkForEvents(self):
        """
        Check for new events pause and stop
        """
        self.notifyObservers()
        if self.pausedEvent.is_set():
            self.waitForContinue()
            self.pausedEvent.clear()
        if self.stoppedEvent.is_set():
            if self.grid.generationNumber != 0:
                self.grid.clearGrid(update=True)
            self.waitForContinue()
            self.stoppedEvent.clear()
        self.notifyObservers()

    def clickGridItem(self, x, y):
        self.grid.checkGridItem(x, y)

    def waitForContinue(self):
        """
        Wait for the continue event
        """
        self.continueEvent.wait()
        self.continueEvent.clear()

    def startContinueGrid(self):
        self.continueEvent.set()

    def stopPauseGrid(self):
        """
        Call to stop or pause the grid
        The controller will know how to handle this request
        """
        if self.pausedEvent.is_set():
            self.stoppedEvent.set()
            self.continueEvent.set()
        elif not self.stoppedEvent.is_set():
            self.pausedEvent.set()

    def gridItemSelected(self, x, y):
        self.grid.click(x, y)

    def stopThread(self):
        """
        Stop the GridController thread nicely
        """
        self.stoppedEvent.clear()
        self.pausedEvent.clear()
        self.continueEvent.set()
        ThreadObject.stopThread(self)

    @property
    def state(self):
        """
        :return: False if stopped or paused
        """
        if self.stoppedEvent.is_set() or self.pausedEvent.is_set():
            return False
        return True

    def getData(self):
        return self.state

    def getGenerationCounter(self):
        return self.grid.generationNumber
