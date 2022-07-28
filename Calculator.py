import toga
from toga.style.pack import COLUMN, Pack, RIGHT
import re

BUTTON_WIDTH = 55
BUTTON_HEIGHT = 45
BUTTON_PADDING = 6

DISPLAY_HEIGHT = 80

WINDOW_WIDTH = 4*BUTTON_WIDTH + 5*BUTTON_PADDING
WINDOW_HEIGHT = DISPLAY_HEIGHT + 5*BUTTON_WIDTH + BUTTON_PADDING*6

stack = []

current_number = "0"

display_label = None
previously_clicked = ""

# ─── Compute ────────────────────────────────────────────────────────────────────


def compute():
    """
    Compute gets the currently populated stack and
    computes the final result of it. before returning
    it empties the stack and return th result.
    """
    global stack

    # phase 1
    # in this phase of the computation, the algorithm moves on the
    # computation stack and reduces the multiplications and divisions.
    # for example, lets say we have: [1, "+", 2, "*", 3 ], the
    # algorithm moves on the stack, and when it gets into the i = 3
    # the current index will map to the value "*", it then computes:
    # stack[i - 1] * stack[i + 1] and the replaces the 3 places within
    # the stack with the new "6". doing so it also decreases the size
    # by 2 since [2, "*", 3] is now [6]
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


# ─── Negation Button ────────────────────────────────────────────────────────────


def negation():
    number = float(display_label.text)
    number *= -1
    set_display_text(number)


def set_display_text(x):
    global display_label
    string_value = str(x)
    no_zeros = re.sub(r"\.0+$", "", string_value)
    display_label.text = no_zeros


# ─── Backspace ──────────────────────────────────────────────────────────────────


def bsp():
    """
    Delete Rightmost Character And Recalculate
    """

    display_label.text = display_label.text[:len(display_label.text)-1]


# ─── Event Handling ─────────────────────────────────────────────────────────────


def on_click(button):
    """
    on_click is the main event handler for all buttons in the
    calculator. it detects the button by the `button.id` and
    performs the necessary actions.
    """
    global previously_clicked
    global stack

    # on the case of number buttons
    if button.id in "0123456789":
        # display number is 0, replace with newly clicked
        if display_label.text in "+÷-×0":
            set_display_text(button.id)
        # otherwise append to the previous number
        else:
            display_label.text += button.id

    if button.id == ".":
        # only add a decimal place if we don't have it already
        if "." not in display_label.text:
            display_label.text += "."

    if button.id in "+÷-×":
        stack.append(float(display_label.text))
        stack.append(button.id)
        current_number = button.id
        set_display_text(current_number)

    if button.id == "=" and previously_clicked != "=":
        stack.append(float(display_label.text))

        set_display_text(compute())

    if button.id == "⌫":
        print(bsp())

    if button.id == "AC":
        stack = []
        display_label.text = ""

    if button.id == "±":
        negation()

    previously_clicked = button.id

# ─── Add Button To Box ──────────────────────────────────────────────────────────


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
