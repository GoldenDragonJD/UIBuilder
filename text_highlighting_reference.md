# Terminal Text Highlighting & Styling Reference

This document provides a reference for ANSI escape sequences used to format, color, and highlight text in the terminal. This is particularly useful for TUI elements that need to indicate focus, such as highlighting the background of an input field or reversing the colors of selected text.

## Basic Syntax

An ANSI escape sequence for styling starts with the escape character followed by a bracket `\033[`, then one or more format codes separated by semicolons, and ends with `m`.

In Python, you print these sequences before the text you want to format, and you **must** remember to reset the formatting afterward so it doesn't bleed into other UI elements.

```python
# \033[7m turns on reverse video (highlighting)
# \033[0m resets all formatting back to normal
print("\033[7mHighlighted Text\033[0m")
```

## Highlighting (Reverse Video)

The simplest way to highlight text or an input bar when it comes into focus is using the **Reverse Video** attribute. This swaps the foreground and background colors of the terminal.

| Action | Escape Sequence | Description |
| :--- | :--- | :--- |
| **Enable Highlight (Reverse)** | `\033[7m` | Swaps foreground and background colors. Great for focused input fields. |
| **Disable Highlight (Reverse)**| `\033[27m` | Turns off reverse video specifically. |
| **Reset All Formatting** | `\033[0m` | Resets all text attributes, including color and highlights. |

### Example: Highlighting an Input Bar
If you have an input bar that is 20 characters wide, you can highlight the empty spaces as well by printing spaces with the reverse attribute enabled:
```python
input_text = "Hello"
bar_length = 20
# Pad the input text with spaces to fill the bar
padded_text = input_text.ljust(bar_length)

# Print the highlighted bar
print(f"\033[7m{padded_text}\033[0m")
```

## Text Formatting Attributes

You can apply other formatting attributes to make your TUI stand out.

| Attribute | Enable Sequence | Disable Sequence |
| :--- | :--- | :--- |
| **Bold** | `\033[1m` | `\033[22m` (or reset `\033[0m`) |
| **Dim** | `\033[2m` | `\033[22m` |
| **Italic** | `\033[3m` | `\033[23m` |
| **Underline** | `\033[4m` | `\033[24m` |
| **Blinking** | `\033[5m` | `\033[25m` |
| **Hidden / Invisible**| `\033[8m` | `\033[28m` |
| **Strikethrough** | `\033[9m` | `\033[29m` |

## Standard Colors (Foreground & Background)

You can specify specific text colors (foreground) and highlight colors (background). 

| Color | Foreground | Background |
| :--- | :--- | :--- |
| **Black** | `\033[30m` | `\033[40m` |
| **Red** | `\033[31m` | `\033[41m` |
| **Green** | `\033[32m` | `\033[42m` |
| **Yellow** | `\033[33m` | `\033[43m` |
| **Blue** | `\033[34m` | `\033[44m` |
| **Magenta** | `\033[35m` | `\033[45m` |
| **Cyan** | `\033[36m` | `\033[46m` |
| **White** | `\033[37m` | `\033[47m` |
| **Default**| `\033[39m` | `\033[49m` |

### Combining Multiple Attributes

You can combine multiple styles by separating the codes with a semicolon. 
For example, to get **Bold White Text** on a **Blue Background**:

```python
# 1 = Bold, 37 = White Text, 44 = Blue Background
print("\033[1;37;44mFocused Input Field\033[0m")
```

## Extended Colors (256-Color Mode)

Modern terminals support 256 colors. You can use these for more nuanced highlighting.

- **Foreground:** `\033[38;5;<ID>m`
- **Background:** `\033[48;5;<ID>m`

*(Where `<ID>` is a number from 0 to 255).*

```python
# Highlight the bar with a dark gray background (ID 235)
print("\033[48;5;235m       Empty Bar Highlight       \033[0m")
```

## True Color (RGB)

Many modern terminals also support 24-bit True Color (RGB).

- **Foreground:** `\033[38;2;<R>;<G>;<B>m`
- **Background:** `\033[48;2;<R>;<G>;<B>m`

```python
# Custom RGB background highlight (e.g., a subtle blue)
print("\033[48;2;50;100;150m Custom Highlight Color \033[0m")
```
