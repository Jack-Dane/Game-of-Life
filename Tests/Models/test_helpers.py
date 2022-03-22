
from unittest import TestCase
from unittest.mock import Mock

from gameOfLife.Models.helpers import iterateGrid


class FunctionMockWrap(Mock):

    def __init__(self):
        super(FunctionMockWrap, self).__init__()
        self.rows = 10
        self.columns = 10
        self.functionCallCount = 0
        self.notifiedObservers = False

    @iterateGrid
    def function(self, x, y):
        self.functionCallCount += 1

    def notifyObservers(self):
        self.notifiedObservers = True


class Test_iterateGrid(TestCase):

    def test(self):
        objectMock = FunctionMockWrap()

        objectMock.function()

        self.assertEqual(objectMock.functionCallCount, 100)
        self.assertFalse(objectMock.notifiedObservers)

    def test_update(self):
        objectMock = FunctionMockWrap()

        objectMock.function(update=True)

        self.assertEqual(objectMock.functionCallCount, 100)
        self.assertTrue(objectMock.notifiedObservers)
