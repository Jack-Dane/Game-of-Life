
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
        """
        Initialise a 2d array of GridItem objects into the self.grid
        """
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
        """
        Clears the grid item specified by the x and y values
        :param x: X coordinate to clear
        :param y: Y coordinate to clear
        """
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
        """
        Update the grid item to next generation value
        :param x: X coordinate
        :param y: Y coordinate
        """
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
        """
        Count the number of surrounding gridItems
        :param x: X coordinate of the selected gridItem
        :param y: Y coordinate of the selected gridItem
        :return: The number of active gridItems surrounding the current gridItem
        """
        surroundCount = 0
        for x2 in range(x-1, x+2):
            for y2 in range(y-1, y+2):
                if not (x2 == x and y2 == y):
                    surroundCount += self.getActiveStatusFromGridItems(x2, y2)
        return surroundCount

    def getActiveStatusFromGridItems(self, x, y):
        """
        Get the active status of the specific grid item
        If the x and y coordinates are out of range, False is returned by default
        :param x: X coordinate of gridItem
        :param y: Y coordinate of gridItem
        :return: True if active, False if not
        """
        try:
            if not (x < 0 or y < 0):
                return self.grid[y][x].active
        except IndexError:
            pass
        return False

    def checkSame(self):
        """
        Check to see if the grid will be the same as the next iteration
        """
        for y in range(self.rows):
            for x in range(self.columns):
                if not self.grid[y][x].checkSame():
                    return False
        return True

    def getData(self):
        return self.grid

    def checkGridItem(self, x, y):
        """
        Toggle a gridItem object
        :param x: X coordinate of the grid item
        :param y: Y coordinate of the grid item
        """
        self.grid[y][x].toggleActive()
