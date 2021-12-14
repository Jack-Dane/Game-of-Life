import time

from Views.printView import PrintView
from Controllers.gridController import GridController
from Models.grid import Grid


def main():
    view = PrintView()
    grid = Grid(30, 100)
    grid.createGrid()
    grid.addObserver(view)

    gridController = GridController(grid)
    gridController.start()


if __name__ == "__main__":
    main()
