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
