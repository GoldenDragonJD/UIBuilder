# Font Size Reference for TUI

In a standard Terminal User Interface (TUI) like the one built with `UIBuilder`, everything is rendered on a fixed 2D grid of character cells (`self.ui.grid`). Because of this architecture, **you cannot change the actual font size (e.g., 12pt to 16pt) of an individual `Label` or text element via Python code.**

However, you have a few alternatives depending on what you want to achieve:

## 1. Global Terminal Font Size (The True Font Size)
The actual size of characters is controlled entirely by the user's terminal emulator (e.g., Windows Terminal, iTerm2, GNOME Terminal, Alacritty). 
* **How to change it:** The user must manually zoom in/out (often using `Ctrl` + `+` or `Ctrl` + `-`), or change their terminal settings.
* **Impact:** This changes the font size of *everything* in the application uniformly.

## 2. "Large Text" via ASCII Art Fonts (Recommended for Titles)
If you want a specific label (like a header or title) to be visibly larger than regular text, you can draw it across multiple rows and columns using block characters.

You can achieve this by implementing a new UI element that generates ASCII art text (e.g., using a Python library like `pyfiglet`), or by manually providing a multi-line string.

*Example of a multi-cell "large" label:*
```text
 ██╗  ██╗███████╗██╗     ██╗      ██████╗ 
 ██║  ██║██╔════╝██║     ██║     ██╔═══██╗
 ███████║█████╗  ██║     ██║     ██║   ██║
 ██╔══██║██╔══╝  ██║     ██║     ██║   ██║
 ██║  ██║███████╗███████╗███████╗╚██████╔╝
 ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ 
```
*How to implement:* You would need to create a `LargeLabel(Element)` class that splits a multi-line ASCII art string by `\n`, and adds it to the grid row by row:
```python
class LargeLabel(Element):
    def add_to_grid(self):
        lines = self.text.split('\n')
        for y_offset, line in enumerate(lines):
            for x_offset, char in enumerate(line):
                self.ui.grid[self.location_y + y_offset][self.location_x + x_offset] = char
```

## 3. DEC Double-Height / Double-Width Line Attributes (Not Recommended)
The VT100 terminal standard includes specific ANSI escape codes to make an entire row of text double-width or double-height. 

* `\033#3` : Top half of a double-height line
* `\033#4` : Bottom half of a double-height line
* `\033#6` : Double-width line

**Why you shouldn't use this:**
1. It applies to the *entire row* of the terminal, so you cannot have regular-sized text and double-sized text on the same `y` level.
2. It completely breaks the fixed X/Y grid alignment logic in `UIBuilder`.
3. Support across modern terminal emulators is very inconsistent (many just ignore it entirely).

## Summary
To make a specific `Label` look bigger in a TUI, you must span the text across multiple grid cells using ASCII text art (Option 2). You cannot modify the point-size of the font rendering programmatically for an individual element.
