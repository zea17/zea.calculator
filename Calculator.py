import toga
from toga.style.pack import COLUMN, Pack

BUTTON_WIDTH = 55
BUTTON_HEIGHT = 45
BUTTON_PADDING = 6

DISPLAY_HEIGHT = 80

WINDOW_WIDTH = 4*BUTTON_WIDTH + 5*BUTTON_PADDING
WINDOW_HEIGHT = DISPLAY_HEIGHT + 5*BUTTON_WIDTH + BUTTON_PADDING*6


def add_button_to_box(box, is_left_most, text):
    left_padding = 0
    if is_left_most:
        left_padding = BUTTON_PADDING
    button = toga.Button(text, style=Pack(
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        padding=BUTTON_PADDING,
        padding_left=left_padding,
    ))
    box.add(button)


def create_main_window_content(app):
    box = toga.Box()
    add_button_to_box(box, True, "⌫")
    add_button_to_box(box, False, "±")
    add_button_to_box(box, False, "%")
    add_button_to_box(box, False, "÷")
    return box


class ExampleWindow(toga.App):
    def quit(self, x):
        self.exit()

    def startup(self):
        self.window = toga.Window(
            size=(250, 340),
            title="Zea Calc",
            resizeable=False,
            on_close=self.quit,
        )
        self.window.app = self
        self.window.content = create_main_window_content(self)
        self.window.show()


def main():
    return ExampleWindow("Calculator", "zea.calculator")


if __name__ == '__main__':
    main().main_loop()
