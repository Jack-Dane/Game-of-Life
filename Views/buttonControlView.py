
from abc import ABC, abstractmethod
import pygame

from Views.frame import Frame
from Views.view import View
from Views.helpers import ensureScreen
from Observers.listener import Listener


class ButtonControlView(Frame, View):

    def __init__(self):
        super(ButtonControlView, self).__init__()
        pygame.font.init()
        self.startButton = None
        self.stopButton = None

    @ensureScreen
    def drawButtons(self):
        self.startButton.draw()
        self.stopButton.draw()

    def checkClicked(self, mousePosition):
        self.startButton.checkCollision(mousePosition)
        self.stopButton.checkCollision(mousePosition)

    def addScreen(self, screen):
        Frame.addScreen(self, screen)
        self.startButton = self.createButton("start")
        self.stopButton = self.createButton("stop/pause")
        self.drawButtons()

    def addController(self, controller):
        View.addController(self, controller)

    def notify(self, subject):
        pass

    def createButton(self, buttonName):
        if buttonName == "start":
            return StartContinueButton(
                self.controller, (0, 61, 6), 5, 0, self.screen, self.offsetX, self.offsetY
            )
        elif buttonName == "stop/pause":
            return StopPauseButton(
                self.controller, (166, 71, 0), 205, 0, self.screen, self.offsetX, self.offsetY
            )
        raise NotImplemented()


class Drawable(ABC):

    def __init__(self, x, y, screen, offsetX, offsetY):
        self.screen = screen
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self):
        raise NotImplementedError()


class Button(Drawable):

    def __init__(self, color, *args):
        super(Button, self).__init__(*args)
        self.drawObject = None
        self.color = color

    def draw(self):
        self.drawObject = pygame.draw.rect(
            self.screen,
            self.color,
            pygame.Rect(
                self.x + self.offsetX,
                self.y + self.offsetY,
                190,
                30
            )
        )

    def checkCollision(self, mousePosition):
        if self.drawObject.collidepoint(mousePosition):
            self.click()

    def click(self):
        raise NotImplementedError()


class Text(Drawable):

    def __init__(self, *args, text=""):
        super(Text, self).__init__(*args)
        self._text = text
        self.font = pygame.font.SysFont("Ariel", 18)
        self.fontColor = 255, 255, 255

    def draw(self):
        self.screen.blit(
            self.font.render(self._text, True, self.fontColor),
            (50 + self.offsetX + self.x, 10 + self.offsetY + self.y)
        )


class TextButton(Button, Text, ABC):

    def __init__(self, color, *args):
        Button.__init__(self, color, *args)
        Text.__init__(self, *args)

    def draw(self):
        Button.draw(self)
        Text.draw(self)


class StopPauseButton(TextButton, Listener):

    def __init__(self, controller, *args):
        super(StopPauseButton, self).__init__(*args)
        self.controller = controller
        self.controller.addObserver(self)
        self._text = "Pause"

    def click(self):
        self.controller.stopPauseGrid()

    def notify(self, subject):
        if subject.getData():
            self._text = "Pause"
        else:
            self._text = "Stop"
        self.draw()


class StartContinueButton(TextButton, Listener):

    def __init__(self, controller, *args):
        super(StartContinueButton, self).__init__(*args)
        self.controller = controller
        self.controller.addObserver(self)
        self._text = "Start"

    def click(self):
        self.controller.startContinueGrid()

    def notify(self, subject):
        self.draw()
