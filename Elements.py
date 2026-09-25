from Border import Border
from UIBuilder import *


class Element:
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y) -> None:
        self.ui = uiBuilder
        self.location_x = location_x
        self.location_y = location_y
        self.is_active = True
        self.is_interactive = False
        self.events = []
        self.name = ""

    @staticmethod
    def add_highlight(buffer):
        for i, ch in enumerate(buffer):
            buffer[i] = f"\033[7m{ch}"


class ProgressBar(Element):
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y, size):
        super().__init__(uiBuilder, location_x, location_y)
        self.size = size
        self.locations = [(location_x + i, location_y) for i in range(size)]
        self.progress = 0
        self.total_progress = 100
        self.name = "ProgressBar"

    def change_progress(self, progress):
        self.progress = progress
        if self.progress >= self.total_progress:
            self.progress = self.total_progress
        elif self.progress <= 0:
            self.progress = 0

    def add_to_grid(self):
        current_progress = []

        for i in range(self.size):
            if i < int(self.size * self.progress / self.total_progress):
                current_progress.append("█")
            else:
                current_progress.append("░")

        for i, loc in enumerate(self.locations):
            self.ui.grid[loc[1]][loc[0]] = (
                current_progress[i] if self.is_active else " "
            )


class Label(Element):
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y, text):
        super().__init__(uiBuilder, location_x, location_y)
        self.text = text
        self.max_length = self.ui.grid_size_x - location_x - 1
        self.name = "Label"

    def add_to_grid(self):
        self.text = UIBuilder.truncate_text(self.text, self.max_length)
        for i in range(self.max_length):
            self.ui.grid[self.location_y][self.location_x + i] = (
                (self.text[i] if i < len(self.text) else " ") if self.is_active else " "
            )


class Input(Element):
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y, size=6) -> None:
        super().__init__(uiBuilder, location_x, location_y)
        self.placeholder = ""
        self.is_interactive = True
        self.input_buffer = []
        self.size = size
        self.grid = [[" " for _ in range(self.size + 2)] for _ in range(3)]
        self.focus = False
        self.border_type = Border.LIGHT
        self.enter_func = lambda *_, **__: None
        self.events = [self.on_enter, self.on_text_changed]
        self.old_text = []
        self.name = "Input"
        self.to_render = []
        self.where_to_place = 0

    def add_to_grid(self):
        UIBuilder.add_border(self.grid, self.border_type)

        self.render_input()

        for loc_y in range(len(self.grid)):
            for loc_x in range(len(self.grid[loc_y])):
                self.ui.grid[loc_y + self.location_y][loc_x + self.location_x] = (
                    (self.grid[loc_y][loc_x]) if self.is_active else " "
                )

    def render_input(self):
        # self.placeholder = UIBuilder.truncate_text(self.placeholder, self.size)
        border_left = self.grid[1][0]
        border_right = self.grid[1][-1]
        self.grid[1] = [border_left] + self.to_render + [border_right]  # pyright: ignore[reportOperatorIssue]

    def on_enter(self):
        if (
            self.ui.current_event.type == Event.KEY_PRESS
            and self.ui.current_event.value == "ENTER"
            and self.focus
        ):
            self.enter_func(self)

    def on_text_changed(self):
        if "".join(self.input_buffer) == "".join(self.old_text):
            return

        self.old_text = UIBuilder.deepcopy(self.input_buffer)

    def on_focus(self):
        to_use_input = (
            self.input_buffer
            if self.input_buffer
            else UIBuilder.truncate_text(self.placeholder, self.size)
        )

        if self.focus:
            self.capture_input()
            if len(to_use_input) > self.size:
                difference = len(to_use_input) - self.size + 1
                self.to_render = to_use_input[0 + difference :] + [" "]
            elif len(to_use_input) == self.size and len(self.input_buffer) == self.size:
                self.to_render = to_use_input[1:] + [" "]
            else:
                self.to_render = list("".join(to_use_input).ljust(self.size))
            Element.add_highlight(self.to_render)
        else:
            if self.to_render:
                self.to_render[0].replace("\033[27m", "")
            if len(to_use_input) > self.size:
                self.to_render = to_use_input[: self.size :]
            else:
                self.to_render = list("".join(to_use_input).ljust(self.size))

    def capture_input(self):
        if self.ui.current_event.type != Event.KEY_PRESS:
            return

        char = self.ui.current_event.value

        if char == "BACK" and self.input_buffer:
            self.input_buffer.pop(self.where_to_place - 1)
            self.where_to_place -= 1 if self.where_to_place > 0 else 0
        elif char == "LEFT":
            self.where_to_place = (
                self.where_to_place - 1 if self.where_to_place > 0 else 0
            )
        elif char == "RIGHT":
            self.where_to_place = (
                self.where_to_place + 1
                if self.where_to_place < len(self.input_buffer)
                else len(self.input_buffer)
            )
        elif len(char) == 1:  # pyright: ignore[reportArgumentType]
            if self.where_to_place == len(self.input_buffer):
                self.input_buffer.append(char)
                self.where_to_place += 1
            else:
                self.input_buffer.insert(self.where_to_place, char)
                self.where_to_place += 1
