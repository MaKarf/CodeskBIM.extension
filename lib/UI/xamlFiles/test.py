from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

from System.Windows import RoutedEventHandler


class PrefixShowWindow(BaseWPFClass):

    def __init__(self, xaml_file_name, parser_class=None):
        BaseWPFClass.__init__(self, xaml_file_name, parser_class)

        # Attach the event handler to the button's "Click" event
        button_run = self.Window.FindName("button_run")
        button_run.Click += RoutedEventHandler(self.button_run_click)

        start_count_textbox = self.Window.FindName("field_start_count")
        if start_count_textbox:
            start_count_textbox.Text = "10"

        self.ShowDialog()

    # Define the event handler for the button clic
    def button_run_click(self, sender, e):
        # Access the "field_start_count" TextBox control
        start_count_textbox = self.Window.FindName("field_start_count")

        # Get the value of the TextBox
        if start_count_textbox:
            start_count_value = start_count_textbox.Text
            print("Start Count:", start_count_value)
        else:
            print("TextBox 'field_start_count' not found.")
