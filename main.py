
from Views.printView import PrintView
from Views.gridView import GridView
from Controllers.gridController import GridController
from Models.grid import Grid


def main():
    view = PrintView()
    uiView = GridView()
    grid = Grid(30, 30)
    grid.createGrid()
    grid.addObserver(view)
    grid.addObserver(uiView)

    gridController = GridController(grid)
    gridController.start()


if __name__ == "__main__":
    main()
