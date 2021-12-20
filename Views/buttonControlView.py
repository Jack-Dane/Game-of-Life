
import pygame
from Views.frame import Frame
from Views.view import View
from Views.helpers import ensureScreen


class ButtonControlView(Frame, View):

    def __init__(self):
        super(ButtonControlView, self).__init__()
        self.controller = None
        self.startButton = ButtonCreator.createButton("start")
        self.stopButton = ButtonCreator.createButton("stop")
        self.pauseButton = ButtonCreator.createButton("pause")

    @ensureScreen
    def drawButtons(self):
        self.startButton.drawButton(self.screen, self.offsetX, self.offsetY)
        self.pauseButton.drawButton(self.screen, self.offsetX, self.offsetY)
        self.stopButton.drawButton(self.screen, self.offsetX, self.offsetY)

    def checkClicked(self, mousePosition):
        if self.stopButton.checkCollision(mousePosition):
            self.controller.stopGrid()
        if self.startButton.checkCollision(mousePosition):
            self.controller.continueGrid()
        if self.pauseButton.checkCollision(mousePosition):
            self.controller.pauseGrid()

    def addScreen(self, screen):
        Frame.addScreen(self, screen)
        self.drawButtons()

    def notify(self, subject):
        pass


class ButtonCreator:

    @staticmethod
    def createButton(buttonName):
        if buttonName == "start":
            return Button("start", (0, 61, 6), 5)
        elif buttonName == "stop":
            return Button("stop", (166, 71, 0), 205)
        elif buttonName == "pause":
            return Button("pause", (166, 83, 0), 405)


class Button:

    def __init__(self, name, color, x):
        self.drawObject = None
        self.x = x
        self.y = 0
        self.name = name
        self.color = color

    def checkCollision(self, mousePosition):
        return self.drawObject.collidepoint(mousePosition)

    def drawButton(self, screen, offsetX, offsetY):
        self.drawObject = pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.x + offsetX,
                self.y + offsetY,
                190,
                30
            )
        )
