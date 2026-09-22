# Terminal ANSI Keycodes for Special Keys

When reading keypresses in raw mode in a terminal window, special characters (like arrow keys, function keys, etc.) are typically transmitted as **ANSI escape sequences**. 

An escape sequence always begins with the **Escape** character (ASCII 27, hex `\x1b`, octal `\033`). The codes listed below are the characters that come *immediately after* the Escape character.

For example, when you press the **UP** arrow key, the terminal sends `Escape` followed by `[A`. In code, you'd check for `\x1b[A`.

## Arrow Keys

| Key | Code Sequence (after `\x1b`) |
| :--- | :--- |
| Up Arrow | `[A` |
| Down Arrow | `[B` |
| Right Arrow | `[C` |
| Left Arrow | `[D` |

## Modified Arrow Keys

| Key | Shift | Alt (Meta) | Ctrl | Ctrl + Shift |
| :--- | :--- | :--- | :--- | :--- |
| **Up** | `[1;2A` | `[1;3A` | `[1;5A` | `[1;6A` |
| **Down** | `[1;2B` | `[1;3B` | `[1;5B` | `[1;6B` |
| **Right**| `[1;2C` | `[1;3C` | `[1;5C` | `[1;6C` |
| **Left** | `[1;2D` | `[1;3D` | `[1;5D` | `[1;6D` |

## Navigation / Editing Keys

| Key | Standard Code | Alternative Code (rxvt/some terms) |
| :--- | :--- | :--- |
| Home | `[H` | `[1~` |
| End | `[F` | `[4~` |
| Insert | `[2~` | |
| Delete | `[3~` | |
| Page Up | `[5~` | |
| Page Down | `[6~` | |

## Function Keys

*Note: F1-F4 often use the letter `O` instead of `[`, while F5 and above use `[` and end with a `~`.*

| Key | Code Sequence |
| :--- | :--- |
| F1 | `OP` (or `[11~`) |
| F2 | `OQ` (or `[12~`) |
| F3 | `OR` (or `[13~`) |
| F4 | `OS` (or `[14~`) |
| F5 | `[15~` |
| F6 | `[17~` |
| F7 | `[18~` |
| F8 | `[19~` |
| F9 | `[20~` |
| F10 | `[21~` |
| F11 | `[23~` |
| F12 | `[24~` |

## Standard Control Characters (No Escape Prefix)

These keys typically do not start with the Escape character. They are sent as single byte ASCII control characters.

| Key | Hex / ASCII | String equivalent |
| :--- | :--- | :--- |
| Escape | `\x1b` (27) | `\e` |
| Tab | `\x09` (9) | `\t` |
| Enter / Return | `\x0a` (10) or `\x0d` (13) | `\n` or `\r` |
| Backspace | `\x7f` (127) or `\x08` (8) | `\b` |

## Processing Example (Python)

If you are reading characters one by one (e.g. using `sys.stdin.read(1)` in Python after setting `tty.setraw()`), a typical handler looks like this:

```python
char = sys.stdin.read(1)

if char == '\x1b':  # Start of an escape sequence
    seq1 = sys.stdin.read(1)
    if seq1 == '[':
        seq2 = sys.stdin.read(1)
        if seq2 == 'A':
            print("UP arrow key pressed")
        elif seq2 == 'B':
            print("DOWN arrow key pressed")
        # ... and so on
```
