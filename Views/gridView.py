
import pygame
from Views.view import View


class GridView(View):

    def __init__(self):
        self.res = (600, 600)
        self.screen = pygame.display.set_mode(self.res)

    def drawGrid(self, subject):
        for row in range(0, subject.rows):
            for column in range(0, subject.columns):
                gridItem = subject.grid[row][column]
                pygame.draw.rect(
                    self.screen,
                    gridItem.color,
                    pygame.Rect(
                        20 * column,
                        20 * row,
                        18,
                        18
                    )
                )
        pygame.display.flip()

    def notify(self, subject):
        self.drawGrid(subject)
