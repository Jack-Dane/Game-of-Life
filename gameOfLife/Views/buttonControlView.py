
from abc import ABC, abstractmethod
import pygame

from gameOfLife.Views.frame import Frame
from gameOfLife.Views.view import View
from gameOfLife.Views.helpers import ensureScreen
from gameOfLife.Observers.observer import Observer


class ButtonControlView(Frame, View):

    def __init__(self):
        super(ButtonControlView, self).__init__()
        pygame.font.init()
        self.startButton = None
        self.stopButton = None
        self.generationCounter = None

    @ensureScreen
    def drawButtons(self):
        self.startButton.draw()
        self.stopButton.draw()
        self.generationCounter.draw()

    def checkClicked(self, mousePosition):
        self.startButton.checkCollision(mousePosition)
        self.stopButton.checkCollision(mousePosition)

    def addScreen(self, screen):
        """
        Call to add the screen to the view which will then create the objects to draw
        :param screen: Screen to add
        """
        Frame.addScreen(self, screen)
        self.startButton = self.createDrawable("start")
        self.stopButton = self.createDrawable("stop/pause")
        self.generationCounter = self.createDrawable("genCounter")
        self.drawButtons()

    def addController(self, controller):
        View.addController(self, controller)

    def notify(self, subject):
        if self.generationCounter:
            self.generationCounter.updateGenerationCounter()

    def createDrawable(self, name):
        """
        Returns a Drawable object differing depending on the name parameter
        :param name: name of the object to return
        :return: Drawable object instance
        """
        if name == "start":
            return StartContinueButton(
                self.controller, (0, 61, 6), 5, 0, self.screen, self.offsetX, self.offsetY
            )
        elif name == "stop/pause":
            return StopPauseButton(
                self.controller, (166, 71, 0), 205, 0, self.screen, self.offsetX, self.offsetY
            )
        elif name == "genCounter":
            return GenerationCounter(
                self.controller, 405, 0, self.screen, self.offsetX, self.offsetY
            )
        raise NotImplementedError()


class Drawable(ABC):

    def __init__(self, x, y, screen, offsetX, offsetY):
        self.screen = screen
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self):
        """
        Method to draw the drawable object
        """
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
        """
        Check to see if the button has been clicked
        :param mousePosition: (x, y) click position
        """
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
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            pygame.Rect(
                50 + self.offsetX + self.x,
                10 + self.offsetY + self.y - 1,
                self._backgroundWidth,
                self._backgroundHeight
            )
        )
        self.screen.blit(
            self.font.render(self._text, True, self.fontColor),
            (50 + self.offsetX + self.x, 10 + self.offsetY + self.y)
        )

    @property
    def _backgroundWidth(self):
        return 0

    @property
    def _backgroundHeight(self):
        return self.font.get_height()


class TextButton(Button, Text, ABC):

    def __init__(self, color, *args):
        Button.__init__(self, color, *args)
        Text.__init__(self, *args)

    def draw(self):
        Button.draw(self)
        Text.draw(self)


class GenerationCounter(Text):

    def __init__(self, controller, *args):
        super(GenerationCounter, self).__init__(*args)
        self.controller = controller
        self._setText()

    def updateGenerationCounter(self):
        self._setText()
        self.draw()

    def _setText(self):
        self._text = f"Evolution N.O: {self.controller.getGenerationCounter()}"

    @property
    def _backgroundWidth(self):
        return 120


class StopPauseButton(TextButton, Observer):

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


class StartContinueButton(TextButton, Observer):

    def __init__(self, controller, *args):
        super(StartContinueButton, self).__init__(*args)
        self.controller = controller
        self.controller.addObserver(self)
        self._text = "Start"

    def click(self):
        self.controller.startContinueGrid()

    def notify(self, subject):
        self.draw()
