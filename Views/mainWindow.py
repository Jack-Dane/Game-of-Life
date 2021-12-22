import sys

import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT
from threading import Thread


class MainWindow(Thread):

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

    def run(self):
        while True:
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
