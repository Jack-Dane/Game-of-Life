
from unittest import TestCase
from unittest.mock import MagicMock, patch

from Views.gridView import GridView


class GridTests(TestCase):

    def setUp(self):
        self.gridView = GridView()
        self.gridView.screen = MagicMock()
        self.gridView.offsetX = 0
        self.gridView.offsetY = 0
        gridItemViews = []
        for row in range(4):
            row = []
            for column in range(4):
                gridItemMock = MagicMock()
                gridItemMock.checkClicked.return_value = False
                row.append(gridItemMock)
            gridItemViews.append(row)
        self.gridView.gridItemViews = gridItemViews


class Test_GridView_drawGrid(GridTests):

    def test_ok(self):
        self.gridView.drawGrid()

        for row in self.gridView.gridItemViews:
            for magicMock in row:
                magicMock.draw.assert_called_once_with(
                    self.gridView.screen, self.gridView.offsetX, self.gridView.offsetY
                )


@patch("Views.gridView.GridItemView", return_value="gridViewItem")
class Test_GridView_initSubject(TestCase):

    def test_ok(self, gridViewItem):
        subject = MagicMock(rows=4, columns=4)
        subject.grid = MagicMock()
        gridView = GridView()
        gridView.screen = MagicMock()

        gridView.initSubject(subject)

        for row in range(4):
            for column in range(4):
                # making sure that all grid items have been requested
                subject.grid.__getitem__.assert_any_call(row)
                subject.grid[row].__getitem__.assert_any_call(row)
                gridViewItem.assert_any_call(column, row, 18, 18, subject.grid[row][column])


class Test_GridView_checkClicked(GridTests):

    def test_miss(self):
        self.gridView.checkClicked((10, 10))

        for row in self.gridView.gridItemViews:
            for gridItem in row:
                gridItem.checkClicked.assert_called_once_with((10, 10))

    def test_hit(self):
        controller = MagicMock()
        self.gridView.controller = controller
        clickedGridItemView = MagicMock()
        clickedGridItemView.checkClicked.return_value = True
        clickedGridItemView.x = 1
        clickedGridItemView.y = 1
        self.gridView.gridItemViews[1][1] = clickedGridItemView
        self.gridView.offsetX = 10
        self.gridView.offsetY = 10

        self.gridView.checkClicked((10, 10))

        for row in range(len(self.gridView.gridItemViews)):
            for column in range(row):
                if row <= 1 and column <= 1:
                    self.gridView.gridItemViews[row][column].checkClicked.assert_called_once_with((10, 10))
                else:
                    self.gridView.gridItemViews[row][column].checkClicked.assert_not_called()
        clickedGridItemView.draw.assert_called_once_with(self.gridView.screen, 10, 10)
        controller.clickGridItem.assert_called_once_with(1, 1)
