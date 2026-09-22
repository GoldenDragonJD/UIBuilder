import atexit
import sys
import threading


class UIBuilder:
    def __init__(self, grid_size_x = 80, grid_size_y = 20):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.grid = [[' ' for _ in range(grid_size_x)] for _ in range(grid_size_y)]
        self.ui_elements = []
        self.interactice_elements = []
        self.last_update = self.deepcopy(self.grid)
        self.run = True
        self.events = []
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
        if element.is_interactive:
            self.interactice_elements.append(element)

    def Loop(self, func, *args, **kwargs):
        for event in self.events:
            threading.Thread(event, daemon=True)
        while self.run:
            func(*args, **kwargs)

    def ExitLoop(self):
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

    @staticmethod
    def getchar():
        try:
            import msvcrt
            return msvcrt.getch().decode('utf-8', 'ignore')
        except ImportError:
            import termios
            import tty

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)

            try:
                tty.setcbreak(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            return ch

    @staticmethod
    def read_key():
        ch = UIBuilder.getchar()
        if ch == '\x1b':
            import select
            if select.select([sys.stdin], [], [], 0.1)[0]:
                seq = sys.stdin.read(2)
                if seq == '[A': return "UP"
                elif seq == '[B': return "DOWN"
                elif seq == '[C': return "RIGHT"
                elif seq == '[D': return "LEFT" 
            return 'ESC'
        elif ch == '\x09': return "TAB"
        elif ch == '\x0a': return "ENTER"
        elif ch == '\x7f': return "BACK"
        return ch


class Event:
    def __init__(self, type, value) -> None:
        self.type = type 
        self.value = value