import toga
from toga.style.pack import COLUMN, Pack, RIGHT

BUTTON_WIDTH = 55
BUTTON_HEIGHT = 45
BUTTON_PADDING = 6

DISPLAY_HEIGHT = 80

WINDOW_WIDTH = 4*BUTTON_WIDTH + 5*BUTTON_PADDING
WINDOW_HEIGHT = DISPLAY_HEIGHT + 5*BUTTON_WIDTH + BUTTON_PADDING*6

stack = []

current_number = "0"


display_label = None


def compute():

    global stack
    size = len(stack)
    i = 0

    while i < size:

        if stack[i] == "÷" or stack[i] == "×":
            op = stack[i]
            left = stack[i - 1]
            right = stack[i + 1]
            result = 0

            if op == "÷":
                result = left / right

            else:
                print("left", left, "right", right)
                result = left * right
            stack = stack[:i - 1] + [result] + stack[i + 2:]
            size -= 2

        i += 1

    result = stack[0]
    for j in range(2, size, 2):
        if stack[j-1] == "+":
            result += stack[j]
        if stack[j-1] == "-":
            result -= stack[j]
    stack = []
    return result


def bsp():

    display_label.text = display_label.text[:len(display_label.text)-1]


previously_clicked = ""


def on_click(button):

    global previously_clicked

    if button.id in "0123456789":
        if display_label.text == "0":
            display_label.text = button.id
        else:
            display_label.text += button.id
        previously_clicked = button.id

    if button.id == ".":
        if "." not in display_label.text:
            display_label.text += "."
        previously_clicked = button.id

    if button.id in "+÷-×":
        stack.append(float(display_label.text))
        stack.append(button.id)
        current_number = "0"
        display_label.text = current_number
        previously_clicked = button.id

    if button.id == "=" and previously_clicked != "=":
        stack.append(float(display_label.text))

        display_label.text = compute()
        previously_clicked = button.id

    if button.id == "⌫":
        print(bsp())


def add_button_to_box(box, is_left_most, text, width=BUTTON_WIDTH):

    left_padding = 0
    if is_left_most:
        left_padding = BUTTON_PADDING
    button = toga.Button(
        text,
        id=text,
        on_press=on_click,
        style=Pack(
            width=width,
            height=BUTTON_HEIGHT,
            padding=BUTTON_PADDING,
            padding_left=left_padding,
            padding_top=0,
            font_size=19,
        ),
    )
    box.add(button)


def create_display(box):
    global display_label

    display_label = toga.Label(
        "0",
        style=Pack(
            text_align=RIGHT,
            font_size=40,
            font_weight="normal",
            padding_right=BUTTON_PADDING,
            padding_top=BUTTON_PADDING*4,
            padding_bottom=BUTTON_PADDING*1.7
        ),
    )

    box.add(display_label)


def create_main_window_content(app):

    box = toga.Box(style=Pack(direction=COLUMN))
    create_display(box)
    line_1 = toga.Box()
    add_button_to_box(line_1, True, "AC")
    add_button_to_box(line_1, False, "⌫")
    add_button_to_box(line_1, False, "±")
    add_button_to_box(line_1, False, "÷")
    box.add(line_1)

    line_2 = toga.Box()
    add_button_to_box(line_2, True, "7")
    add_button_to_box(line_2, False, "8")
    add_button_to_box(line_2, False, "9")
    add_button_to_box(line_2, False, "×")
    box.add(line_2)

    line_3 = toga.Box()
    add_button_to_box(line_3, True, "4")
    add_button_to_box(line_3, False, "5")
    add_button_to_box(line_3, False, "6")
    add_button_to_box(line_3, False, "-")
    box.add(line_3)

    line_4 = toga.Box()
    add_button_to_box(line_4, True, "1")
    add_button_to_box(line_4, False, "2")
    add_button_to_box(line_4, False, "3")
    add_button_to_box(line_4, False, "+")
    box.add(line_4)

    line_5 = toga.Box()
    add_button_to_box(line_5, True, "0", width=2*BUTTON_WIDTH+BUTTON_PADDING)
    add_button_to_box(line_5, False, ".")
    add_button_to_box(line_5, False, "=")
    box.add(line_5)
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
