
from unittest import TestCase
from unittest.mock import patch, MagicMock

from gameOfLife.Views.buttonControlView import (
    ButtonControlView, StartContinueButton, StopPauseButton, GenerationCounter, Button, Text
)


@patch("pygame.font.init")
class Test_ButtonControlView_createDrawable(TestCase):

    def setUp(self):
        self.buttonControlView = ButtonControlView()
        self.buttonControlView.controller = MagicMock()
        self.buttonControlView.screen = MagicMock()
        self.buttonControlView.offsetX = 0
        self.buttonControlView.offsetY = 0

    def test_start_button(self, _pygame_font_init):
        startButton = self.buttonControlView.createDrawable("start")

        self.assertIsInstance(startButton, StartContinueButton)

    def test_stop_pause_button(self, _pygame_font_init):
        stopPauseButton = self.buttonControlView.createDrawable("stop/pause")

        self.assertIsInstance(stopPauseButton, StopPauseButton)

    def test_generation_counter(self, _pygame_font_init):
        generationCounter = self.buttonControlView.createDrawable("genCounter")

        self.assertIsInstance(generationCounter, GenerationCounter)


class ButtonTests(TestCase):

    def setUp(self):
        self.screen = MagicMock()
        self.button = Button((0, 0, 0), 10, 10, self.screen, 50, 20)


class Test_Button_draw(ButtonTests):

    @patch("pygame.draw.rect", return_value="drawRectangle")
    @patch("pygame.Rect", return_value="rectangle")
    def test_correct_values(self, pygame_Rect, pygame_draw_rect):
        self.button.draw()

        pygame_Rect.assert_called_once_with(60, 30, 190, 30)
        pygame_draw_rect.assert_called_once_with(self.screen, (0, 0, 0), "rectangle")
        self.assertEqual(self.button.drawObject, "drawRectangle")


class Test_Button_checkCollision(ButtonTests):

    def setUp(self):
        super(Test_Button_checkCollision, self).setUp()
        self.button.drawObject = MagicMock()
        self.button.click = MagicMock()

    def test_hit(self):
        self.button.drawObject.collidepoint.return_value = True

        self.button.checkCollision((10, 30))

        self.button.click.assert_called_once_with()

    def test_miss(self):
        self.button.drawObject.collidepoint.return_value = False

        self.button.checkCollision((10, 30))

        self.button.click.assert_not_called()


class Test_Text_draw(TestCase):

    def setUp(self):
        pass

    @patch("pygame.font.SysFont")
    @patch("pygame.draw.rect", return_value="drawRectangle")
    @patch("pygame.Rect", return_value="rectangle")
    def test_ok(self, pygame_rect, pygame_draw_rect, pygame_font_SysFont):
        self.screen = MagicMock()
        self.text = Text(10, 10, self.screen, 50, 20, text="Test")
        self.text.font.get_height.return_value = 600
        self.text.font.render = MagicMock(return_value="text_render")

        self.text.draw()

        pygame_draw_rect.assert_called_once_with(self.screen, (0, 0, 0), "rectangle")
        pygame_rect.assert_called_once_with(110, 39, 0, 600)
        self.text.font.render.assert_called_once_with("Test", True, (255, 255, 255))
        self.screen.blit.assert_called_once_with("text_render", (110, 40))


class Test_StopPauseButton_notify(TestCase):

    def setUp(self):
        self.pygame_font_SysFont = patch("pygame.font.SysFont")
        self.pygame_font_SysFont.start()

        self.screen = MagicMock()
        self.controller = MagicMock()
        self.stopPauseButton = StopPauseButton(self.controller, (0, 0, 0), 10, 10, self.screen, 50, 20)
        self.stopPauseButton.draw = MagicMock()

    def tearDown(self):
        self.pygame_font_SysFont.stop()

    def test_pause(self):
        subject = MagicMock()
        subject.getData.return_value = True

        self.stopPauseButton.notify(subject)

        self.assertEqual(self.stopPauseButton._text, "Pause")
        self.stopPauseButton.draw.assert_called_once_with()

    def test_stop(self):
        subject = MagicMock()
        subject.getData.return_value = False

        self.stopPauseButton.notify(subject)

        self.assertEqual(self.stopPauseButton._text, "Stop")
        self.stopPauseButton.draw.assert_called_once_with()
