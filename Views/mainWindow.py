import sys

import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT
from Threads.thread import ThreadObject


class MainWindow(ThreadObject):

    def __init__(self):
        super(MainWindow, self).__init__()
        pygame.init()
        self.res = (620, 660)
        self.screen = pygame.display.set_mode(self.res)
        self.frames = []

    def addFrame(self, frame):
        frame.addScreen(self.screen)
        self.frames.append(frame)

    def checkClicked(self, mousePosition):
        for frame in self.frames:
            frame.checkClicked(mousePosition)

    def loopExecution(self):
        self.checkEvents()
        pygame.display.flip()

    def checkEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                self.checkClicked(mousePosition)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit(0)

    def stopThread(self):
        super(MainWindow, self).stopThread()
        pygame.quit()
