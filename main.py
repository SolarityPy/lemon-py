import dearpygui.dearpygui as dpg

# Format for button callbacks is button name, then callback
def open_configuration_callback():
    dpg.show_item("file_dialog_id")
    
# Triggered when the user selects a file in the Explorer dialog
def file_dialog_callback(sender, app_data):
    path = app_data['file_path_name']
    print(path)

# ImGui Initialization
dpg.create_context()
dpg.create_viewport(title="Lemon", width=400, height=250, clear_color=(240, 240, 240, 255))
dpg.setup_dearpygui()

# Adds font to ImGui
with dpg.font_registry():
    default_font = dpg.add_font("./Roboto-Regular.ttf", 20)
    
# Initializes main Lemon window
with dpg.window(label="Lemon", no_title_bar=True, pos=(0, 0), width=400, height=250, no_move=True):
    dpg.bind_font(default_font) # Sets the Roboto Regular font
    
    # Adds Open Config button and shows the file dialog by calling the callback function
    dpg.add_button(label="Open Configuration", callback=open_configuration_callback)
    
    dpg.add_file_dialog(
        directory_selector=True, show=False, callback=file_dialog_callback, 
        tag="file_dialog_id", width=700 ,height=400
    )

# Starts display main loop
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()