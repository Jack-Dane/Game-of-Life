
import pygame
from gameOfLife.Views.view import View
from gameOfLife.Views.frame import Frame
from gameOfLife.Views.helpers import ensureScreen
from gameOfLife.Observers.observer import Observer


class GridView(View, Frame, Observer):

    def __init__(self):
        Frame.__init__(self)
        View.__init__(self)
        self.gridItemViews = []
        self.subject = None

    @ensureScreen
    def drawGrid(self):
        """
        draw each of the gridItems
        """
        for row in self.gridItemViews:
            for gridItemView in row:
                gridItemView.draw(
                    self.screen,
                    self.offsetX,
                    self.offsetY,
                )

    @ensureScreen
    def initSubject(self, subject):
        """
        create the grid item array based on the model/subject
        :param subject: grid model/subject
        """
        for row in range(0, subject.rows):
            rowLst = []
            for column in range(0, subject.columns):
                gridItem = subject.grid[row][column]
                gridItemView = GridItemView(
                    column,
                    row,
                    18,
                    18,
                    gridItem
                )
                rowLst.append(gridItemView)
            self.gridItemViews.append(rowLst)

    def notify(self, subject):
        """ Update function that is called when the grid has been updated
        If the grid array is empty initialise it
        """
        if not self.gridItemViews:
            self.initSubject(subject)
        self.drawGrid()

    def addScreen(self, screen):
        Frame.addScreen(self, screen)

    @ensureScreen
    def checkClicked(self, mousePosition):
        for rows in self.gridItemViews:
            for gridItemView in rows:
                if gridItemView.checkClicked(mousePosition):
                    self.controller.clickGridItem(gridItemView.x, gridItemView.y)
                    gridItemView.draw(self.screen, self.offsetX, self.offsetY)
                    return  # no need to search any others


class GridItemView:

    def __init__(self, x, y, width, height, gridItem):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gridItem = gridItem
        self.color = gridItem.color
        self.gridButton = None

    def draw(self, screen, offsetX, offsetY):
        self.gridButton = pygame.draw.rect(
            screen,
            self.gridItem.color,
            pygame.Rect(
                ((self.height + 2) * self.x) + offsetX,
                ((self.width + 2) * self.y) + offsetY,
                self.width,
                self.height
            )
        )

    def checkClicked(self, mousePos):
        return self.gridButton.collidepoint(mousePos)
