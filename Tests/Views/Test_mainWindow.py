
from unittest import TestCase
from unittest.mock import patch, MagicMock
from pygame.locals import MOUSEBUTTONDOWN, QUIT

from Views.mainWindow import MainWindow


class Test_MainWindow_checkEvents(TestCase):

    def setUp(self):
        self.threadObjectPatch = patch("Views.mainWindow.ThreadObject")
        self.threadObjectPatch.start()
        self.pygamePatch = patch("Views.mainWindow.pygame")
        self.pygame = self.pygamePatch.start()

        self.mainWindow = MainWindow()
        self.mainWindow.checkClicked = MagicMock()

    def tearDown(self):
        self.threadObjectPatch.stop()
        self.pygamePatch.stop()

    def test_MOUSEBUTTONDOWN(self):
        self.pygame.mouse.get_pos.return_value = (50, 50)
        self.pygame.event.get.return_value = [MagicMock(type=MOUSEBUTTONDOWN)]

        self.mainWindow.checkEvents()

        self.mainWindow.checkClicked.assert_called_once_with((50, 50))

    @patch("sys.exit")
    def test_QUIT(self, sys_exit):
        self.pygame.event.get.return_value = [MagicMock(type=QUIT)]

        self.mainWindow.checkEvents()

        self.pygame.quit.assert_called_once()
        sys_exit.assert_called_once_with(0)

    def test_unrecognised_input(self):
        self.pygame.event.get.return_value = [MagicMock(type=5000)]

        self.mainWindow.checkEvents()

        self.pygame.quit.assert_not_called()
        self.mainWindow.checkClicked.assert_not_called()
