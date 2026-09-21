# Python Terminal Input & Mouse Detection Reference

This document provides a reference for detecting keyboard presses and mouse events in a Linux/Unix terminal using only the Python Standard Library (no third-party libraries or `curses`), building on ANSI escape sequences.

## 1. Detecting Key Presses

By default, the terminal is in "cooked" mode, meaning input is buffered until you press `Enter`. To detect individual key presses instantly, you must change the terminal to "raw" or "cbreak" mode using the built-in `sys`, `tty`, and `termios` modules.

### Basic Non-Blocking Key Press Reader

```python
import sys
import tty
import termios

def getch():
    """Reads a single character from standard input without requiring Enter."""
    fd = sys.stdin.fileno()
    # Save current terminal settings
    old_settings = termios.tcgetattr(fd)
    try:
        # Change terminal to cbreak mode (read 1 char at a time, don't echo)
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
    finally:
        # Always restore settings to avoid breaking the terminal
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
```

### Detecting Special Keys (Arrows, Home, End)

Special keys like arrow keys generate ANSI escape sequences (a sequence of characters starting with the Escape character `\033` or `\x1b`).

```python
def read_key():
    ch = getch()
    if ch == '\x1b':  # Escape character
        # Need to read the next two characters for arrow keys
        # Set a very short timeout to differentiate between single ESC and an escape sequence
        import select
        if select.select([sys.stdin], [], [], 0.1)[0]:
            seq = sys.stdin.read(2)
            if seq == '[A': return 'UP'
            if seq == '[B': return 'DOWN'
            if seq == '[C': return 'RIGHT'
            if seq == '[D': return 'LEFT'
        return 'ESC'
    return ch
```

## 2. Detecting Mouse Events

To receive mouse events, you must send an ANSI escape sequence to the terminal to tell it to start reporting mouse clicks. When the user clicks, the terminal will send an escape sequence back to `sys.stdin`, exactly like a special key press!

### Enabling Mouse Reporting

| Action | Escape Sequence | Description |
| :--- | :--- | :--- |
| **Enable Normal Mouse** | `\033[?1000h` | Reports clicks and releases. |
| **Enable Any Event** | `\033[?1003h` | Reports clicks, releases, and motion. |
| **SGR Extended Mode** | `\033[?1006h` | Modern format supporting coords > 223. |

*To disable mouse reporting, use `l` instead of `h` (e.g., `\033[?1000l`).*

### Decoding the Mouse Input

When SGR mode (`1006h`) is enabled, a click generates an escape sequence looking like this:
`\033[<B;X;YM` (Button pressed) or `\033[<B;X;Ym` (Button released).

* **B**: Button code (0=Left, 1=Middle, 2=Right, 64=Scroll Up, 65=Scroll Down)
* **X / Y**: 1-based coordinates of the mouse click

### Full Example: Keyboard & Mouse Loop

```python
import sys
import tty
import termios

# Constants for enabling/disabling mouse tracking
# 1000h = Normal tracking (clicks/releases)
# 1006h = SGR formatting (better for larger coordinates)
ENABLE_MOUSE = "\033[?1000h\033[?1006h"
DISABLE_MOUSE = "\033[?1000l\033[?1006l"

def main():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    print(ENABLE_MOUSE, end="", flush=True)
    print("\033[2J\033[H", end="") # Clear screen
    print("Click anywhere or press 'q' to quit.")
    
    try:
        tty.setcbreak(fd)
        while True:
            ch = sys.stdin.read(1)
            
            if ch == 'q':
                break
                
            if ch == '\x1b': # Escape sequence starts
                seq1 = sys.stdin.read(1)
                if seq1 == '[':
                    seq2 = sys.stdin.read(1)
                    if seq2 == '<':
                        # Mouse event detected (SGR format)
                        event = ""
                        while True:
                            c = sys.stdin.read(1)
                            event += c
                            if c in ('M', 'm'): # 'M' is press, 'm' is release
                                break
                                
                        # event now looks like "0;10;5M"
                        parts = event[:-1].split(';')
                        button = int(parts[0])
                        x = int(parts[1])
                        y = int(parts[2])
                        action = "Pressed" if event[-1] == 'M' else "Released"
                        
                        btn_name = "Left" if button == 0 else "Middle" if button == 1 else "Right" if button == 2 else f"Btn{button}"
                        
                        # Print status at top of screen
                        print(f"\033[s\033[2;1H\033[KMouse: {btn_name} {action} at ({x}, {y})\033[u", end="", flush=True)
                    else:
                        # Arrow keys or other sequences
                        print(f"\033[s\033[3;1H\033[KKey sequence: ESC [ {seq2}\033[u", end="", flush=True)
            else:
                # Regular characters
                print(f"\033[s\033[4;1H\033[KKey pressed: {ch}\033[u", end="", flush=True)
    finally:
        # CRITICAL: Always disable mouse and restore terminal state on exit
        print(DISABLE_MOUSE, end="", flush=True)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
```

## Important Notes

1. **Always restore state:** If your script crashes while the terminal is in `cbreak` mode, or while mouse reporting is enabled, your terminal might act broken until you type the `reset` command. Using `try...finally` blocks (as shown above) or the `atexit` module (like in your `UIBuilder.py`) is highly recommended.
2. **`sys.stdin.read(1)` is blocking:** The loop will pause waiting for input. If your UI requires constant background updating (e.g., a progress bar animation like in `test.py`), you need non-blocking input. You can achieve this using the `select` module:

```python
import select

def kbhit():
    """Returns True if a key or mouse event is waiting to be read."""
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    return len(dr) > 0

# Inside your loop:
# if kbhit():
#     process_input()
# update_ui()
```
