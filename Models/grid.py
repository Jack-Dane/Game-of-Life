
from Models.gridItem import GridItem
from Observers.subject import Subject
from Models.helpers import iterateGrid


class Grid(Subject):

    def __init__(self, rows, columns):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.same = False
        self.generationNumber = 0
        self.createGrid()

    def createGrid(self):
        self.grid = []
        for row in range(self.rows):
            fullRow = []
            for column in range(self.columns):
                fullRow.append(
                    GridItem(row, column)
                )
            self.grid.append(fullRow)

    @iterateGrid
    def clearGrid(self, x, y):
        self.grid[y][x].markInactive(nextIteration=True)
        self.generationNumber = 0

    def update(self, updateGeneration=True):
        """
        Update the list items to reflect the game of life
        """
        self.updateGridItem()
        self.same = self.checkSame()
        self.updateAllGridItemsNextIteration()
        if updateGeneration:
            self.generationNumber += 1
        self.notifyObservers()

    @iterateGrid
    def updateGridItem(self, x, y):
        currentItem = self.grid[y][x]
        totalSurrounding = self.countSurroundingActiveGridItems(x, y)
        currentItem.shouldChange(totalSurrounding)

    @iterateGrid
    def updateAllGridItemsNextIteration(self, x, y):
        self.grid[y][x].update()

    def click(self, x, y):
        self.grid[y][x].toggleActive()

    def start(self):
        self.update(updateGeneration=False)

    def countSurroundingActiveGridItems(self, x, y):
        surroundCount = 0
        for x2 in range(x-1, x+2):
            for y2 in range(y-1, y+2):
                if not (x2 == x and y2 == y):
                    surroundCount += self.getActiveStatusFromGridItems(x2, y2)
        return surroundCount

    def getActiveStatusFromGridItems(self, x, y):
        try:
            if not (x < 0 or y < 0):
                return self.grid[y][x].active
        except IndexError:
            pass
        return False

    def checkSame(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if not self.grid[x][y].checkSame():
                    return False
        return True

    def getData(self):
        return self.grid

    def checkGridItem(self, x, y):
        self.grid[y][x].toggleActive()
