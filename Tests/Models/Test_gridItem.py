
from unittest import TestCase
from unittest.mock import MagicMock

from Models.gridItem import GridItem


class GridItemTests(TestCase):

    def setUp(self):
        self._gridItem = GridItem(0 ,0)


class Test_GridItem_Color(GridItemTests):

    def test_color_active(self):
        self._gridItem.active = True

        color = self._gridItem.color

        self.assertEqual(color, (170, 170, 170))

    def test_color_inactive(self):
        color = self._gridItem.color

        self.assertEqual(color, (0, 0, 0))


class Test_GridItem_MarkInactive(GridItemTests):

    def setUp(self):
        super(Test_GridItem_MarkInactive, self).setUp()
        self._gridItem.active = True
        self._gridItem.nextIteration = True

    def test_mark_inactive(self):
        self._gridItem.markInactive()

        self.assertFalse(self._gridItem.active)
        self.assertTrue(self._gridItem.nextIteration)

    def test_mark_inactive_next_iteration(self):
        self._gridItem.markInactive(nextIteration=True)

        self.assertFalse(self._gridItem.active)
        self.assertFalse(self._gridItem.nextIteration)


class Test_GridItem_toggleActive(GridItemTests):

    def test_toggle_active(self):
        self._gridItem.active = True

        self._gridItem.toggleActive()

        self.assertFalse(self._gridItem.active)

    def test_toggle_inactive(self):
        self._gridItem.toggleActive()

        self.assertTrue(self._gridItem.active)


class Test_GridItem_ShouldChange(GridItemTests):

    def setUp(self):
        super(Test_GridItem_ShouldChange, self).setUp()
        self._gridItem.shouldDie = MagicMock()
        self._gridItem.shouldReproduce = MagicMock()

    def test_should_change_active(self):
        self._gridItem.active = True

        self._gridItem.shouldChange(5)

        self._gridItem.shouldDie.assert_called_once_with(5)

    def test_should_change_inactive(self):
        self._gridItem.shouldChange(5)

        self._gridItem.shouldReproduce.assert_called_once_with(5)


class Test_GridItem_ShouldDie(GridItemTests):

    def test_in_range(self):
        totalSurroundings = [2, 3]

        for totalSurrounding in totalSurroundings:
            self._gridItem.shouldDie(totalSurrounding)

            self.assertTrue(self._gridItem.nextIteration)

    def test_out_of_range(self):
        totalSurroundings = [0, 1, 4, 5, 6, 7, 8]

        for totalSurrounding in totalSurroundings:
            self._gridItem.shouldDie(totalSurrounding)

            self.assertFalse(self._gridItem.nextIteration)


class Test_GridItem_ShouldReproduce(GridItemTests):

    def test_in_range(self):
        totalSurrounding = 3

        self._gridItem.shouldReproduce(totalSurrounding)

        self.assertTrue(self._gridItem.nextIteration)

    def test_out_of_range(self):
        totalSurroundings = [0, 1, 2, 4, 5, 6, 7, 8]

        for totalSurrounding in totalSurroundings:
            self._gridItem.shouldReproduce(totalSurrounding)

            self.assertFalse(self._gridItem.nextIteration)
