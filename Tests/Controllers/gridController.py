
from unittest import TestCase
from unittest.mock import MagicMock, Mock

from Controllers.gridController import GridController


class GridControllerTests(TestCase):

    def setUp(self):
        self.grid = Mock()
        self.grid.generationNumber = 0
        self._gridController = GridController(self.grid)
        self._gridController.notifyObservers = MagicMock()
        self._gridController.waitForContinue = MagicMock()


class Test_GridController_checkForEvents(GridControllerTests):

    def test_stop_event_generation_zero(self):
        self._gridController.waitForContinue.return_value = True

        self._gridController.checkForEvents()

        self.assertEqual(
            self._gridController.notifyObservers.call_count,
            2
        )
        self._gridController.waitForContinue.assert_called_once_with()
        self.assertFalse(self._gridController.stoppedEvent.is_set())
        self.grid.clearGrid.assert_not_called()

    def test_stop_event_not_generation_zero(self):
        self._gridController.waitForContinue.return_value = True
        self.grid.generationNumber = 10

        self._gridController.checkForEvents()

        self.assertEqual(
            self._gridController.notifyObservers.call_count,
            2
        )
        self.grid.clearGrid.assert_called_once_with(update=True)
        self._gridController.waitForContinue.assert_called_once_with()
        self.assertFalse(self._gridController.stoppedEvent.is_set())

    def test_pause_event_continue_event(self):
        self._gridController.stoppedEvent.clear()
        self._gridController.pausedEvent.set()
        self._gridController.waitForContinue.return_value = True

        self._gridController.checkForEvents()

        self.assertEqual(
            self._gridController.notifyObservers.call_count,
            2
        )
        self._gridController.waitForContinue.assert_called_once_with()
        self.assertFalse(self._gridController.pausedEvent.is_set())


class Test_GridController_stopPauseGrid(GridControllerTests):

    def test_pause_event(self):
        self._gridController.stoppedEvent.clear()

        self._gridController.stopPauseGrid()

        self.assertTrue(self._gridController.pausedEvent.is_set())

    def test_stop_event(self):
        self._gridController.pausedEvent.set()

        self._gridController.stopPauseGrid()

        self.assertTrue(self._gridController.stoppedEvent.is_set())
        self.assertTrue(self._gridController.continueEvent.is_set())


class Test_GridController_state(GridControllerTests):

    def test_paused_state(self):
        self._gridController.stoppedEvent.clear()
        self._gridController.pausedEvent.set()

        state = self._gridController.state

        self.assertFalse(state)

    def test_stopped_state(self):
        self._gridController.stoppedEvent.set()
        self._gridController.pausedEvent.clear()

        state = self._gridController.state

        self.assertFalse(state)

    def test_stopped_and_paused_state(self):
        self._gridController.stoppedEvent.set()
        self._gridController.pausedEvent.set()

        state = self._gridController.state

        self.assertFalse(state)

    def test_not_stopped_or_paused_state(self):
        self._gridController.stoppedEvent.clear()
        self._gridController.pausedEvent.clear()

        state = self._gridController.state

        self.assertTrue(state)
