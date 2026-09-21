# Python Terminal Cursor Movement Reference

This document provides a reference for ANSI escape sequences used to control the terminal cursor in Python.

## Basic Syntax

An ANSI escape sequence typically starts with the escape character followed by a bracket: `\033[` or `\x1b[`.

In Python, you can print these sequences to the terminal to control the cursor. For example:
```python
print("\033[A", end="")  # Moves the cursor up one line
```

## Cursor Movement Commands

Replace `<N>`, `<R>`, and `<C>` with integers. If omitted, they usually default to `1`.

| Action | Escape Sequence | Example (Python string) | Description |
| :--- | :--- | :--- | :--- |
| **Move Up** | `\033[<N>A` | `\033[5A` | Moves cursor up by N lines. |
| **Move Down** | `\033[<N>B` | `\033[3B` | Moves cursor down by N lines. |
| **Move Right** | `\033[<N>C` | `\033[10C` | Moves cursor forward (right) by N columns. |
| **Move Left** | `\033[<N>D` | `\033[2D` | Moves cursor backward (left) by N columns. |
| **Next Line** | `\033[<N>E` | `\033[1E` | Moves cursor to the beginning of the next Nth line. |
| **Previous Line** | `\033[<N>F` | `\033[2F` | Moves cursor to the beginning of the previous Nth line. |
| **Move to Column**| `\033[<N>G` | `\033[5G` | Moves cursor to column N on the current line. |
| **Set Position** | `\033[<R>;<C>H` | `\033[10;5H` | Moves cursor to row R, column C. (Top-left is `1;1`). |
| **Set Position** | `\033[<R>;<C>f` | `\033[10;5f` | Same as `H` (Move cursor to row R, column C). |

## Cursor State and Clearing

| Action | Escape Sequence | Example (Python string) | Description |
| :--- | :--- | :--- | :--- |
| **Save Position** | `\033[s` | `\033[s` | Saves the current cursor position. |
| **Restore Position**| `\033[u` | `\033[u` | Restores the cursor to the last saved position. |
| **Hide Cursor** | `\033[?25l` | `\033[?25l` | Hides the terminal cursor. |
| **Show Cursor** | `\033[?25h` | `\033[?25h` | Shows the terminal cursor. |
| **Clear Screen** | `\033[2J` | `\033[2J` | Clears the entire screen. |
| **Clear to End** | `\033[0J` | `\033[0J` | Clears from cursor to the end of the screen. |
| **Clear to Start** | `\033[1J` | `\033[1J` | Clears from cursor to the beginning of the screen. |
| **Clear Line** | `\033[2K` | `\033[2K` | Clears the entire current line. |
| **Clear Line End** | `\033[0K` | `\033[0K` | Clears from cursor to the end of the line. |
| **Clear Line Start**| `\033[1K` | `\033[1K` | Clears from cursor to the beginning of the line. |

## Common Patterns: Replacing Text

Here are the most common ways to replace or update text in the terminal without printing new lines.

### 1. Updating the Entire Current Line
Use a carriage return (`\r`) to move to the beginning of the current line and overwrite it.
```python
import time
for i in range(1, 11):
    # \r moves to start of line, end="" prevents a new line
    print(f"\rProcessing item {i}/10...", end="", flush=True)
    time.sleep(0.5)
```

### 2. Clearing Before Replacing (Safest Way)
If you replace a long string with a short one, the end of the old string will remain visible. To fix this, use `\033[K` to clear the rest of the line before printing.
```python
import time
status_messages = ["Initializing...", "Downloading data...", "Done!"]
for msg in status_messages:
    # \r goes to start, \033[K clears the line, then we print the message
    print(f"\r\033[KStatus: {msg}", end="", flush=True)
    time.sleep(1)
```

### 3. Updating a Specific Fixed Coordinate
For dashboards or UI, move to the specific coordinate, clear the line, write the value, and restore the cursor.
```python
def update_value_at(row, col, value):
    # \033[s       -> Save current cursor position
    # \033[{r};{c}H -> Move to specific row and col
    # \033[K       -> Clear from cursor to end of line
    # {value}      -> Print the new value
    # \033[u       -> Restore cursor back to where it was saved
    print(f"\033[s\033[{row};{col}H\033[K{value}\033[u", end="", flush=True)
```

## Notes
- To use these in Python's `print()` function effectively without adding newlines, remember to use `end=""` and potentially `flush=True`.
- Example: `print("\033[2J\033[H", end="", flush=True)` clears the screen and moves the cursor to the top-left (home) position.
