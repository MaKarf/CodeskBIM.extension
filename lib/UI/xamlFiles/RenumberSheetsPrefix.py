from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass, RoutedEventHandler, KeyEventHandler


class RenumberSheetsPrefix(BaseWPFClass):

    def __init__(self):
        BaseWPFClass.__init__(self, xaml_file_name="RenumberSheetsPrefix.xaml")
        self.start = 1
        self.prefix = "0"

        """Access the "field_start_count" TextBox control"""
        self.start_count_textbox = self.Window.FindName("field_start_count")
        self.prefix_textbox = self.Window.FindName("field_prefix")
        self.warning = self.Window.FindName("warning")
        self.block = False

        """Attach the event handler to the button's "Click" event"""
        self.button_run = self.Window.FindName("button_run")
        self.button_run.Click += RoutedEventHandler(self.button_run_click)

        self.start_count_textbox.KeyUp += KeyEventHandler(self.integer_check)

        self.ShowDialog()

    def integer_check(self, sender, e):
        if sender.Text != "":
            if not sender.Text.isdigit():
                self.warning.Text = "Start must be integer"
                self.block = True
            else:
                self.warning.Text = ""
                self.block = False

    def button_run_click(self, sender, e):
        if not self.block:
            """Get the value of the TextBox"""
            if self.start_count_textbox.Text == "":
                self.start = 1
            else:
                self.start = self.start_count_textbox.Text

            self.prefix = self.prefix_textbox.Text
            # print("Start Count: {}".format(self.start))
            # print("Prefix: {}".format(self.prefix))

            self.Close()
