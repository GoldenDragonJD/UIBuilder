import atexit
import sys


class UIBuilder:
    def __init__(self, grid_size_x = 80, grid_size_y = 20):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.grid = [[' ' for _ in range(grid_size_x)] for _ in range(grid_size_y)]
        self.ui_elements = []
        self.last_update = self.deepcopy(self.grid)
        self.old_settings = None
        self.run = True
        atexit.register(self.signal_handler)

    def signal_handler(self):
        print("\033[?25h")
        print("\033[0;0H", end="")
        print(f"\033[{self.grid_size_y}E", end="")

    def deepcopy(self, array):
        return [row[:] for row in array]

    def print_here(self, x, y, char):
        print(f"\033[{x};{y}H", end="")
        print(char, end="", flush=True)

    def add_border_top(self):
        self.grid[0] = ['━' for _ in range(self.grid_size_x)]

    def add_border_bottom(self):
        self.grid[self.grid_size_y - 1] = ['━' for _ in range(self.grid_size_x)]

    def add_border_left(self):
        for row in self.grid:
            row[0] = '┃'
        self.grid[0][0] = '┏'
        self.grid[-1][0] = '┗'

    def add_border_right(self):
        for row in self.grid:
            row[self.grid_size_x - 1] = '┃'
        self.grid[0][-1] = '┓'
        self.grid[-1][-1] = '┛'

    def add_border(self):
        self.add_border_top()
        self.add_border_bottom()
        self.add_border_left()
        self.add_border_right()

    def draw(self):
        print("\033[2J", end="")
        print("\033[0;0H", end="")

        for row in self.grid:
            print(''.join(row))

        print("\033[?25l", end="")

    def draw_change(self):
        for element in self.ui_elements:
            element.add_to_grid()

        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                if self.grid[y][x] != self.last_update[y][x]:
                    self.print_here(y + 1, x + 1, self.grid[y][x])
        self.last_update = self.deepcopy(self.grid)

    def add_ui_element(self, element):
        self.ui_elements.append(element)

    def getchar(self):
        try:
            import msvcrt
            return msvcrt.getch().decode('utf-8', 'ignore')
        except ImportError:
            import termios
            import tty

            fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(fd)

            try:
                tty.setcbreak(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, self.old_settings)

            return ch

    def Loop(self):
        while self.run:
            pass

    def ExitLoog(self):
        self.run = False

    @staticmethod
    def truncate_text(text, max_length):
        if len(text) <= max_length:
            return text

        text = text[:max_length]

        if max_length >= 4:
            text = text[:-3] + "..."
        elif max_length >= 3:
            text = text[:-2] + ".."
        elif max_length >= 2:
            text = text[:-1] + "."

        return text

class ProgressBar:
    def __init__(self, uiBuilder: UIBuilder, location_x, location_y, size):
        self.ui = uiBuilder
        self.location_x = location_x
        self.location_y = location_y
        self.size = size
        self.locations = [(location_x + i, location_y) for i in range(size)]
        self.progress = 0
        self.total_progress = 100

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

    def add_to_grid(self):
        self.text = UIBuilder.truncate_text(self.text, self.max_length)
        for i, char in enumerate(self.text):
            self.ui.grid[self.location_y][self.location_x + i] = char
