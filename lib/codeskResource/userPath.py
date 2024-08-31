# import os
#
#
# def user_path(folder_name=""):
#     path = os.path.join(r"C:", r"{}\{}".format(os.environ['HOMEPATH'], folder_name))
#     if __name__ == "__main__":
#         print(path)
#     return path
#
#
# # if __name__ == "__main__":
#     # user_path("Documents")
#

import Wpf

# Create a list to hold the checkboxes
checkboxes = []


def on_checkbox_click(sender, e):
    global last_clicked_checkbox
    if shift_pressed:
        start_index = checkboxes.index(last_clicked_checkbox)
        end_index = checkboxes.index(sender)
        for i in range(min(start_index, end_index), max(start_index, end_index) + 1):
            checkboxes[i].IsChecked = True
    last_clicked_checkbox = sender


def on_key_down(sender, e):
    global shift_pressed
    if e.Key == Wpf.Input.Key.LeftShift or e.Key == Wpf.Input.Key.RightShift:
        shift_pressed = True


def on_key_up(sender, e):
    global shift_pressed
    if e.Key == Wpf.Input.Key.LeftShift or e.Key == Wpf.Input.Key.RightShift:
        shift_pressed = False


# Create a WPF window
window = Wpf.Window()
window.Title = "Multiple Selection Example"
window.Width = 300
window.Height = 200

# Create checkboxes and attach click event handlers
for i in range(1, 11):
    checkbox = Wpf.CheckBox()
    checkbox.Content = "Checkbox {}".format(i)
    checkbox.Click += on_checkbox_click
    checkboxes.append(checkbox)
    window.Content = checkbox

# Attach key down and key up event handlers
window.KeyDown += on_key_down
window.KeyUp += on_key_up

# Global variables to track shift state and last clicked checkbox
shift_pressed = False
last_clicked_checkbox = None

# Show the window
window.ShowDialog()
