
from unittest import TestCase
from unittest.mock import MagicMock

from Views.helpers import ensureScreen, NoScreenAssignedException


class TestObject:

    def __init__(self, screen=None):
        self.screen = screen

    @ensureScreen
    def getScreen(self):
        return self.screen


class Test_ensureScreen(TestCase):

    def test_screen_present(self):
        screen = MagicMock()
        testObject = TestObject(screen)

        returnScreen = testObject.getScreen()

        self.assertEqual(screen, returnScreen)

    def test_missing_screen(self):
        testObject = TestObject()

        with self.assertRaises(NoScreenAssignedException):
            testObject.getScreen()
