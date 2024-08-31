import clr

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")

from System.Windows.Controls import StackPanel, Orientation, TextBox, Label
from System.Windows.Input import KeyEventHandler
from System.Windows import Visibility

from lib.UI.xamlFiles.CheckboxSelection import CheckboxSelection


class RenumberSheetsUI(CheckboxSelection):

    def __init__(self, items=None, select_multiple=True, parser_class=None, window_title="Selection Window",
                 window_width=None,
                 selection_name="Select Elements", finish_button_text_name="Finish"):
        CheckboxSelection.__init__(self, items=items, select_multiple=select_multiple, parser_class=parser_class,
                                   window_title=window_title,
                                   window_width=window_width, window_height=630,
                                   selection_name=selection_name, finish_button_text_name=finish_button_text_name)

        self.start_number = ""
        self.prefix = ""

        """lock the finish button if the start number is not set to an integer.
        this will help avoid further errors and error handling"""
        self.lock = False

        """add_top_allowance buttons"""
        self.start_number_label = self.add_button(host_panel=self.bottom_allowance_panel,
                                                  label_name="Start Number", textbox_text="1",
                                                  on_key_up_function=self.start_textbox_key_up)
        self.start_number = "1"

        self.prefix_label = self.add_button(host_panel=self.bottom_allowance_panel,
                                            label_name="Prefix", textbox_text="0",
                                            on_key_up_function=self.prefix_textbox_key_up, )
        self.prefix = "0"

        """hide the error text label if not in used"""
        self.top_error_message.Visibility = Visibility.Collapsed

        self.ShowDialog()

    def prefix_textbox_key_up(self, sender, e):
        self.prefix = sender.Text

    def start_textbox_key_up(self, sender, e):

        if sender.Text.replace(" ", "").isdigit():
            self.start_number = sender.Text.replace(" ", "")
            self.bottom_error_message.Content = ""
            self.lock = False

        elif sender.Text.replace(" ", "") == "":
            self.bottom_error_message.Content = "Start Number will be set to 1 if left empty"

        else:
            self.bottom_error_message.Content = "Start Number must be integer. (example 1 or 2 )"
            self.lock = True

    @staticmethod
    def add_button(host_panel, label_name="Text", textbox_text="", on_key_up_function=None):
        panel = StackPanel()
        panel.Orientation = Orientation.Horizontal

        label = Label()
        label.Content = label_name

        textbox = TextBox()
        textbox.Height = 20
        textbox.Width = 60
        textbox.Text = textbox_text

        """add event handler"""
        if on_key_up_function is not None:
            textbox.KeyUp += KeyEventHandler(on_key_up_function)

        panel.Children.Add(label)
        panel.Children.Add(textbox)
        host_panel.Children.Add(panel)

        return label

    def finish_selection(self, sender, e):
        if not self.lock:
            self.Close()


"""how to use the class"""
if __name__ == "__main__":
    item = [{"name": "Item {}".format(i), "element": i} for i in range(20)]


    def select():
        ui = RenumberSheetsUI(item)
        selection = ui.selected_items
        prefix = ui.prefix
        start = ui.start_number
        if len(selection) != 0:
            print(selection)
        print(prefix)
        print(start)
        return selection


    select()
