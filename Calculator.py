import toga
from toga.style.pack import COLUMN, Pack


def create_main_window_content(app):
    box = toga.Box()

    return box


class ExampleWindow(toga.App):
    def quit(self, x):
        self.exit()

    def startup(self):
        self.window = toga.Window(
            size=(270, 380),
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
