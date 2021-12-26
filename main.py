import time

from Views.printView import PrintView
from Views.gridView import GridView
from Views.mainWindow import MainWindow
from Views.buttonControlView import ButtonControlView
from Controllers.gridController import GridController
from Models.grid import Grid


threads = []

def main():
    # view = PrintView()
    gridView = GridView()
    buttonControlView = ButtonControlView()
    grid = Grid(30, 30)
    # grid.addObserver(view)
    grid.addObserver(gridView)
    grid.addObserver(buttonControlView)

    gridController = GridController(grid)
    gridView.addController(gridController)
    buttonControlView.addController(gridController)

    mainWindow = MainWindow()
    gridView.setOffset(10, 10)
    mainWindow.addFrame(gridView)
    buttonControlView.setOffset(10, 620)
    mainWindow.addFrame(buttonControlView)

    threads.append(gridController)
    gridController.start()
    threads.append(mainWindow)
    mainWindow.start()

    checkStopEvent()


def checkStopEvent():
    try:
        while True:
            time.sleep(.2)
    except KeyboardInterrupt:
        for thread in threads:
            thread.stopThread()
            thread.join()


if __name__ == "__main__":
    main()
