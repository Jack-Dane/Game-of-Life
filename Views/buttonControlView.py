
import pygame
from Views.frame import Frame
from Views.view import View
from Views.helpers import ensureScreen


class ButtonControlView(Frame, View):

    def __init__(self):
        super(ButtonControlView, self).__init__()
        pygame.font.init()
        self.startButton = None
        self.stopButton = None

    @ensureScreen
    def drawButtons(self):
        self.startButton.draw(self.screen, self.offsetX, self.offsetY)
        self.stopButton.draw(self.screen, self.offsetX, self.offsetY)

    def checkClicked(self, mousePosition):
        self.startButton.checkCollision(mousePosition)
        self.stopButton.checkCollision(mousePosition)

    def addScreen(self, screen):
        Frame.addScreen(self, screen)
        self.drawButtons()

    def addController(self, controller):
        View.addController(self, controller)
        self.startButton = ButtonCreator.createButton("start", self.controller)
        self.stopButton = ButtonCreator.createButton("stop/pause", self.controller)

    def notify(self, subject):
        """
        Easy way to know when to update the text on the buttons
        Would be better to listen to the controller directly though
        A race condition could occur here where it doesn't get updated
        """
        self.drawButtons()


class ButtonCreator:

    @staticmethod
    def createButton(buttonName, controller):
        if buttonName == "start":
            return StartContinueButton(controller, (0, 61, 6), 5, 0)
        elif buttonName == "stop/pause":
            return StopPauseButton(controller, (166, 71, 0), 205, 0)
        raise NotImplemented()


class Button:

    def __init__(self, color, x, y):
        self.drawObject = None
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen, offsetX, offsetY):
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

    def checkCollision(self, mousePosition):
        if self.drawObject.collidepoint(mousePosition):
            self.click()

    def click(self):
        raise NotImplementedError()


class Text:

    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self._text = text
        self.font = pygame.font.SysFont("Ariel", 18)
        self.fontColor = 255, 255, 255

    @property
    def text(self):
        return self._text

    def draw(self, screen, offsetX, offsetY):
        screen.blit(
            self.font.render(self.text, True, self.fontColor),
            (50 + offsetX + self.x, 10 + offsetY + self.y)
        )


class TextButton(Button, Text):

    def __init__(self, *args):
        Button.__init__(self, *args)
        Text.__init__(self, *args)

    @property
    def text(self):
        return ""

    def draw(self, screen, offsetX, offsetY):
        Button.draw(self, screen, offsetX, offsetY)
        Text.draw(self, screen, offsetX, offsetY)


class StopPauseButton(TextButton):

    def __init__(self, controller, *args):
        super(StopPauseButton, self).__init__(*args)
        self.controller = controller

    def click(self):
        self.controller.stopPauseGrid()

    @property
    def text(self):
        if self.controller.state:
            return "Pause"
        return "Stop"


class StartContinueButton(TextButton):

    def __init__(self, controller, *args):
        super(StartContinueButton, self).__init__(*args)
        self.controller = controller

    def click(self):
        self.controller.startContinueGrid()

    @property
    def text(self):
        return "Start"
