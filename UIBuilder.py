import atexit
import os
import sys
import threading
import time

from Border import Border


class UIBuilder:
    def __init__(self, grid_size_x=80, grid_size_y=20, location_x=0, location_y=0):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.location_x = location_x
        self.location_y = location_y
        self.grid = [[" " for _ in range(grid_size_x)] for _ in range(grid_size_y)]
        self.ui_elements = []
        self.interactice_elements = [self]
        self.last_update = self.deepcopy(self.grid)
        self.run = True
        self.event_buffer = []
        self.main_thread_event_buffer = []
        self.current_event = Event.NoneEvent()
        self.focus = True
        self.name = "UI"

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
        print("\033[0;0H", end="")
        print(f"\033[{self.location_y + self.grid_size_y}E", end="")

    def on_focus(self):
        if not self.focus: return
        print('\033[?25l', end="")

    def cycle_focus(self):
        if (
            self.current_event.type == Event.KEY_PRESS
            and self.current_event.value == "TAB"
        ):
            first_element = self.interactice_elements.pop(0)
            self.interactice_elements.append(first_element)

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
                    self.print_here(0, 0, '\033[0m')
                    self.print_here(x + 1, y + 1, self.grid[y][x])
        self.last_update = self.deepcopy(self.grid)

    def add_ui_element(self, element):
        self.ui_elements.append(element)
        if element.is_interactive:
            self.interactice_elements.append(element)

    def Loop(self, func, *args, **kwargs):
        threading.Thread(
            target=UIBuilder.event_read_keys, args=(self,), daemon=True
        ).start()

        while self.run:
            if self.event_buffer:
                self.main_thread_event_buffer.append(self.event_buffer.pop(0))

            self.current_event = (
                self.main_thread_event_buffer[0]
                if self.main_thread_event_buffer
                else Event.NoneEvent()
            )

            self.cycle_focus()

            for element in self.interactice_elements:
                element.focus = False

            self.interactice_elements[0].focus = True

            for element in self.interactice_elements:
                element.on_focus()

            for element in self.ui_elements:
                for event in element.events:
                    event()

            func(*args, **kwargs)

            if self.main_thread_event_buffer:
                self.main_thread_event_buffer.pop(0)

            self.draw_change()
            time.sleep(0.01)

    def ExitLoop(self):
        self.run = False

    @staticmethod
    def deepcopy(array):
        return [row[:] for row in array]

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

            return msvcrt.getch().decode("utf-8", "ignore")
        except ImportError:
            fd = sys.stdin.fileno()
            return os.read(fd, 1).decode("utf-8", "ignore")

    @staticmethod
    def read_key():
        ch = UIBuilder.getchar()

        # 1. Windows: msvcrt sends \xe0 or \x00 before an arrow key, not \x1b
        if ch in ("\xe0", "\x00"):
            c2 = UIBuilder.getchar()
            if c2 == "H":
                return "UP"
            if c2 == "P":
                return "DOWN"
            if c2 == "M":
                return "RIGHT"
            if c2 == "K":
                return "LEFT"
            return "ESC"

        # 2. Linux/macOS: Standard ANSI escape sequences (\x1b[A)
        if ch == "\x1b":
            import select

            if select.select([sys.stdin], [], [], 0.05)[0]:
                c1 = UIBuilder.getchar()
                if c1 == "[" or c1 == "O":
                    seq = c1
                    while True:
                        if len(seq) > 1 and (seq[-1].isalpha() or seq[-1] == "~"):
                            break
                        if select.select([sys.stdin], [], [], 0.01)[0]:
                            seq += UIBuilder.getchar()
                        else:
                            break
                    
                    ansi_map = {
                        "[A": "UP", "[B": "DOWN", "[C": "RIGHT", "[D": "LEFT",
                        "[1;2A": "SHIFT_UP", "[1;3A": "ALT_UP", "[1;5A": "CTRL_UP", "[1;6A": "CTRL_SHIFT_UP",
                        "[1;2B": "SHIFT_DOWN", "[1;3B": "ALT_DOWN", "[1;5B": "CTRL_DOWN", "[1;6B": "CTRL_SHIFT_DOWN",
                        "[1;2C": "SHIFT_RIGHT", "[1;3C": "ALT_RIGHT", "[1;5C": "CTRL_RIGHT", "[1;6C": "CTRL_SHIFT_RIGHT",
                        "[1;2D": "SHIFT_LEFT", "[1;3D": "ALT_LEFT", "[1;5D": "CTRL_LEFT", "[1;6D": "CTRL_SHIFT_LEFT",
                        "[H": "HOME", "[1~": "HOME",
                        "[F": "END", "[4~": "END",
                        "[2~": "INSERT",
                        "[3~": "DELETE",
                        "[5~": "PAGE_UP",
                        "[6~": "PAGE_DOWN",
                        "OP": "F1", "[11~": "F1",
                        "OQ": "F2", "[12~": "F2",
                        "OR": "F3", "[13~": "F3",
                        "OS": "F4", "[14~": "F4",
                        "[15~": "F5",
                        "[17~": "F6",
                        "[18~": "F7",
                        "[19~": "F8",
                        "[20~": "F9",
                        "[21~": "F10",
                        "[23~": "F11",
                        "[24~": "F12",
                        "Op": "0", "Oq": "1", "Or": "2", "Os": "3", "Ot": "4",
                        "Ou": "5", "Ov": "6", "Ow": "7", "Ox": "8", "Oy": "9",
                        "On": ".", "OM": "ENTER", "Om": "-", "Ok": "+", "Ol": "+",
                        "Oj": "*", "Oo": "/"
                    }
                    
                    if seq in ansi_map:
                        return ansi_map[seq]
            return "ESC"

        if ch == "\x09":
            return "TAB"
        if ch in ("\x0a", "\r"):
            return "ENTER"  # Catch \r for Windows
        if ch in ("\x7f", "\x08"):
            return "BACK"  # Catch \x08 for Windows
        return ch

    @staticmethod
    def event_read_keys(ui):
        while ui.run:
            key = UIBuilder.read_key()
            ui.event_buffer.append(Event("key_pressed", key))

    @staticmethod
    def add_border_top(grid, type):
        grid[0] = [
            Border.get_border_chars(type)["horizontal"] for _ in range(len(grid[0]))
        ]

    @staticmethod
    def add_border_bottom(grid, type):
        grid[-1] = [
            Border.get_border_chars(type)["horizontal"] for _ in range(len(grid[0]))
        ]

    @staticmethod
    def add_border_left(grid, type):
        border_chars = Border.get_border_chars(type)
        for row in grid:
            row[0] = border_chars["vertical"]
        grid[0][0] = border_chars["top_left_corner"]
        grid[-1][0] = border_chars["bottom_left_corner"]

    @staticmethod
    def add_border_right(grid, type):
        border_chars = Border.get_border_chars(type)
        for row in grid:
            row[-1] = border_chars["vertical"]
        grid[0][-1] = border_chars["top_right_corner"]
        grid[-1][-1] = border_chars["bottom_right_corner"]

    @staticmethod
    def add_border(grid, type):
        UIBuilder.add_border_bottom(grid, type)
        UIBuilder.add_border_top(grid, type)
        UIBuilder.add_border_left(grid, type)
        UIBuilder.add_border_right(grid, type)


class Event:
    KEY_PRESS = "key_pressed"

    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    @staticmethod
    def NoneEvent():
        return Event("None", None)
