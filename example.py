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