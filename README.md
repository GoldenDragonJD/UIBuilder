# UIBuilder

UIBuilder is a simple terminal UI library that allows you to create interactive text-based user interfaces.

## User-Facing API Documentation

### `UIBuilder` (from `UIBuilder.py`)
The main class that initializes and manages the terminal UI canvas.

- **`__init__(self, grid_size_x=80, grid_size_y=20, location_x=0, location_y=0)`**
  Initializes the UI builder. 
  - `grid_size_x`, `grid_size_y`: The dimensions of the UI grid.
  - `location_x`, `location_y`: The top-left terminal position where the UI will be drawn.
- **`add_ui_element(self, element)`**
  Registers an element (such as a Label, ProgressBar, or Input) to be rendered and managed by the UI.
- **`Loop(self, func, *args, **kwargs)`**
  Starts the main event loop. It clears the screen, sets up input handling, and continuously calls the provided `func` function while rendering changes to the UI.
- **`ExitLoop(self)`**
  Stops the main event loop and prepares the application to exit safely.

### `Elements` (from `Elements.py`)
Various UI components you can add to your UIBuilder instance.

#### `Label`
A simple text component.
- **`__init__(self, uiBuilder, location_x, location_y, text)`**
  Creates a text label.
  - `uiBuilder`: The parent `UIBuilder` instance.
  - `location_x`, `location_y`: Coordinates within the UI grid.
  - `text`: The string to display.

#### `ProgressBar`
A horizontal progress bar.
- **`__init__(self, uiBuilder, location_x, location_y, size)`**
  - `size`: The width of the progress bar in characters.
- **`change_progress(self, progress)`**
  Updates the progress bar. `progress` should be a value between 0 and 100 (which is the default `total_progress`).

#### `Input`
An interactive text input field with an optional border.
- **`__init__(self, uiBuilder, location_x, location_y, max_input=6)`**
  - `max_input`: Maximum number of characters the user can type.
- **Attributes you can modify**:
  - `border_type`: The visual style of the border. Defaults to `Border.LIGHT`.
  - `enter_func`: A callback function triggered when the user presses ENTER while focused on the input. It must accept one argument (the input element itself).
  - `input_buffer`: The list of characters currently typed. You can read it as `"".join(input.input_buffer)`.
  - `placeholder`: The text displayed when the input is empty.

### `Border` (from `Border.py`)
Provides constant styles to customize the border of `Input` elements. Use these with `my_input.border_type = Border.STYLE`.
- `Border.LIGHT`
- `Border.HEAVY`
- `Border.DOUBLE`
- `Border.ROUND`

---

## Example Usage

```python
import time
from UIBuilder import UIBuilder
from Elements import ProgressBar, Label, Input
from Border import Border

# 1. Initialize the UI
ui = UIBuilder(grid_size_x=40, grid_size_y=12, location_x=5, location_y=2)
UIBuilder.add_border(ui.grid, type=Border.ROUND)

# 2. Create Elements
title = Label(ui, 2, 1, "Welcome to UIBuilder!")
ui.add_ui_element(title)

pbar = ProgressBar(ui, 2, 3, 20)
ui.add_ui_element(pbar)

user_input = Input(ui, 2, 5, size=10)
user_input.border_type = Border.ROUND
user_input.placeholder = "Name..."
ui.add_ui_element(user_input)

status_label = Label(ui, 2, 9, "Status: Waiting for input...")
ui.add_ui_element(status_label)

# 3. Define Interactions
def on_enter(input_elem):
    name = "".join(input_elem.input_buffer)
    status_label.text = f"Status: Hello {name}!"
    input_elem.input_buffer.clear()
    input_elem.where_to_place = 0 # reset cursor
    
user_input.enter_func = on_enter

# 4. Define custom loop logic (Runs every ~0.01s)
# Using a dictionary to keep track of state
state = {"ticks": 0, "progress": 0}

def app_logic():
    state["ticks"] += 1
    # Update progress bar slowly
    if state["ticks"] % 10 == 0:
        state["progress"] += 1
        if state["progress"] > 100:
            state["progress"] = 0
        pbar.change_progress(state["progress"])
        
    # Example of exiting loop programmatically
    if "".join(user_input.input_buffer).lower() == "exit":
        ui.ExitLoop()
        
# 5. Run the UI
ui.Loop(app_logic)
```