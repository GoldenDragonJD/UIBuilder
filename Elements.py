from UIBuilder import UIBuilder


class Element:
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y) -> None:
        self.ui = uiBuilder
        self.location_x = location_x
        self.location_y = location_y
        self.is_active = True
        self.is_interactive = False


class ProgressBar(Element):
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y, size):
        super().__init__(uiBuilder, location_x, location_y)
        self.size = size
        self.locations = [(location_x + i, location_y) for i in range(size)]
        self.progress = 0
        self.total_progress = 100
        self.is_interactive = False

    def change_progress(self, progress):
        self.progress = progress
        self.ui.draw_change()

    def add_to_grid(self):
        current_progress = []

        for i in range(self.size):
            if i < int(self.size * self.progress / self.total_progress):
                current_progress.append('█')
            else:
                current_progress.append('░')

        for i, loc in enumerate(self.locations):
            self.ui.grid[loc[1]][loc[0]] = current_progress[i]


class Label:
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y, text):
        self.ui = uiBuilder
        self.location_x = location_x
        self.location_y = location_y
        self.text = text
        self.max_length = self.ui.grid_size_x - location_x - 1
        self.is_interactive = False

    def add_to_grid(self):
        self.text = UIBuilder.truncate_text(self.text, self.max_length)
        for i, char in enumerate(self.text):
            self.ui.grid[self.location_y][self.location_x + i] = char


class Input:
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y) -> None:
        self.ui = uiBuilder
        self.location_x = location_x
        self.location_y = location_y
        self.placeholder = ""
        self.is_interactive = True
