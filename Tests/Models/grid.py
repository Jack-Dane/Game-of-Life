
import random
from unittest import TestCase
from unittest.mock import MagicMock

from Models.grid import Grid
from Models.gridItem import GridItem


class Test_Grid_CreateGrid(TestCase):

    def test(self):
        rows = 40
        columns = 30
        grid = Grid(rows, columns)

        grid.createGrid()

        self.assertEqual(len(grid.grid), rows)
        for rowIndex in range(rows):
            self.assertEqual(len(grid.grid[rowIndex]), columns)
            for columnIndex in range(columns):
                self.assertIsInstance(grid.grid[rowIndex][columnIndex], GridItem)


class GridTests(TestCase):

    def setUp(self):
        self._rows = 4
        self._columns = 3
        self._grid = Grid(self._rows, self._columns)
        self._grid.createGrid()

    def randomiseGridItems(self, nextIteration=False):
        for row in self._grid.grid:
            for gridItem in row:
                active = random.randrange(0, 1)
                gridItem.shouldChange = MagicMock()
                gridItem.active = active
                if nextIteration:
                    gridItem.nextIteration = active


class Test_Grid_ClearGrid(GridTests):

    def test(self):
        self.randomiseGridItems()

        self._grid.clearGrid()

        for row in self._grid.grid:
            for gridItem in row:
                self.assertFalse(gridItem.active)
                self.assertFalse(gridItem.nextIteration)


class Test_Grid_UpdateGridItem(GridTests):

    def test(self):
        self._grid.countSurroundingActiveGridItems = MagicMock()

        self.randomiseGridItems()
        self._grid.updateGridItem()

        for y in range(self._grid.rows):
            for x in range(self._grid.columns):
                self._grid.countSurroundingActiveGridItems.assert_any_call(x, y)
                self._grid.grid[y][x].shouldChange.assert_called_once()


class TestSpecificGridConfiguration(GridTests):

    def setUp(self):
        super(TestSpecificGridConfiguration, self).setUp()
        self.displayGrid = [
            [1, 1, 1],
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        for y in range(self._grid.rows):
            for x in range(self._grid.columns):
                self._grid.grid[y][x].active = self.displayGrid[y][x]


class Test_Grid_CountSurroundingActiveGridItems(TestSpecificGridConfiguration):

    def test(self):
        surroundingCountLst = [
            [1, 2, 1],
            [4, 6, 4],
            [1, 2, 1],
            [2, 3, 2]
        ]

        for y in range(self._grid.rows):
            for x in range(self._grid.columns):
                surroundingCount = self._grid.countSurroundingActiveGridItems(x, y)
                self.assertEqual(surroundingCount, surroundingCountLst[y][x])


class Test_Grid_GetActiveStatusFromGridItems(TestSpecificGridConfiguration):

    def test_correctResult(self):
        for y in range(self._grid.rows):
            for x in range(self._grid.columns):
                status = self._grid.getActiveStatusFromGridItems(x, y)
                self.assertEqual(status, self.displayGrid[y][x])

    def test_indexOutOfRange(self):
        status = self._grid.getActiveStatusFromGridItems(10, 10)

        self.assertEqual(status, False)

    def test_negativeIndex(self):
        status = self._grid.getActiveStatusFromGridItems(-1, -1)

        self.assertEqual(status, False)


class Test_Grid_CheckSame(TestSpecificGridConfiguration):

    def changeNextGridItems(self, grid):
        for y in range(self._rows):
            for x in range(self._columns):
                self._grid.grid[y][x].nextIteration = grid[y][x]

    def test_same_grid(self):
        self.changeNextGridItems(self.displayGrid)

        same = self._grid.checkSame()

        self.assertTrue(same)

    def test_different_grid(self):
        differentGrid = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 0],
            [0, 1, 0]
        ]
        self.changeNextGridItems(differentGrid)

        same = self._grid.checkSame()

        self.assertFalse(same)
