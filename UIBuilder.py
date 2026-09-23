import atexit
import sys
import threading
import time


class UIBuilder:
    def __init__(self, grid_size_x = 80, grid_size_y = 20, location_x = 0, location_y = 0):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.location_x = location_x
        self.location_y = location_y
        self.grid = [[' ' for _ in range(grid_size_x)] for _ in range(grid_size_y)]
        self.ui_elements = []
        self.interactice_elements = []
        self.last_update = self.deepcopy(self.grid)
        self.run = True
        self.event_buffer = []
        self.main_thread_event_buffer = []
        self.current_event = Event.NoneEvent()

        try:
            import termios
            import tty

            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        except ImportError:
            self.old_settings = None
        atexit.register(self.signal_handler)

        self.draw()

    def signal_handler(self):
        if self.old_settings is not None:
            import termios
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        print("\033[?25h")
        print('\033[0;0H', end="")
        print(f'\033[{self.location_y + self.grid_size_y}E', end="")

    def cycle_focus(self):
        if self.current_event.type == Event.KEY_PRESS and self.current_event.value == "TAB":
            first_element = self.interactice_elements.pop(0)
            self.interactice_elements.append(first_element)

    def deepcopy(self, array):
        return [row[:] for row in array]

    def print_here(self, x, y, char):
        print(f"\033[{y + self.location_y};{x + self.location_x}H", end="")
        print(char, end="", flush=True)

    def draw(self):
        print("\033[2J", end="")
        print("\033[?25l", end="")

    def draw_change(self):
        for element in self.ui_elements:
            element.add_to_grid()

        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                if self.grid[y][x] != self.last_update[y][x]:
                    self.print_here(x + 1, y + 1, self.grid[y][x])
        self.last_update = self.deepcopy(self.grid)

    def add_ui_element(self, element):
        self.ui_elements.append(element)
        if element.is_interactive:
            self.interactice_elements.append(element)

    def Loop(self, func, *args, **kwargs):
        threading.Thread(target=UIBuilder.event_read_keys, args=(self,), daemon=True).start()

        while self.run:
            if self.event_buffer:
                self.main_thread_event_buffer.append(self.event_buffer.pop(0))

            self.current_event = self.main_thread_event_buffer[0] if self.main_thread_event_buffer else Event.NoneEvent()

            func(*args, **kwargs)
            self.draw_change()

            if self.main_thread_event_buffer: self.main_thread_event_buffer.pop(0)
            time.sleep(0.01)

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
            return sys.stdin.read(1)

    @staticmethod
    def read_key():
        ch = UIBuilder.getchar()
        if ch == '\x1b':
            seq1 = sys.stdin.read(1)
            if seq1 == '[':
                seq2 = sys.stdin.read(1)
                if seq2 == 'A': return "UP"
                elif seq2 == 'B': return "DOWN"
                elif seq2 == 'C': return "RIGHT"
                elif seq2 == 'D': return "LEFT"

            return 'ESC'
        elif ch == '\x09': return "TAB"
        elif ch == '\x0a': return "ENTER"
        elif ch == '\x7f': return "BACK"
        return ch

    @staticmethod
    def event_read_keys(ui):
        while ui.run:
            key = UIBuilder.read_key()
            ui.event_buffer.append(Event("key_pressed", key))

    @staticmethod
    def add_border_top(grid):
        grid[0] = ['━' for _ in range(len(grid[0]))]

    @staticmethod
    def add_border_bottom(grid):
        grid[-1] = ['━' for _ in range(len(grid[0]))]

    @staticmethod
    def add_border_left(grid):
        for row in grid:
            row[0] = '┃'
        grid[0][0] = '┏'
        grid[-1][0] = '┗'

    @staticmethod
    def add_border_right(grid):
        for row in grid:
            row[-1] = '┃'
        grid[0][-1] = '┓'
        grid[-1][-1] = '┛'

    @staticmethod
    def add_border(grid):
        UIBuilder.add_border_bottom(grid)
        UIBuilder.add_border_top(grid)
        UIBuilder.add_border_left(grid)
        UIBuilder.add_border_right(grid)


class Event:
    KEY_PRESS = "key_pressed"

    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    @staticmethod
    def NoneEvent():
        return Event("None", None)
