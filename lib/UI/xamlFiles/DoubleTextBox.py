import clr

from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

clr.AddReference("System.Windows")

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


class DoubleTextBox(BaseWPFClass):

    def __init__(self, title=None,
                 label_name1=None, label_name2=None,
                 button_name=None):

        self.text_results1 = ""
        self.text_results2 = ""

        BaseWPFClass.__init__(self, xaml_file_name="DoubleTextBox.xaml")

        """Find the "button_run" button by its name"""
        self.label1 = self.Window.FindName("label1")
        self.text_block1 = self.Window.FindName("text1")

        self.label2 = self.Window.FindName("label2")
        self.text_block2 = self.Window.FindName("text2")

        self.button_object = self.Window.FindName("finish_button")

        if title is not None:
            self.Window.Title = title

        if label_name1 is not None:
            self.label1.Text = label_name1

        if label_name2 is not None:
            self.label2.Text = label_name2

        if button_name is not None:
            self.button_object.Content = button_name

        """Attach the event handler to the button's "Click" event"""
        # self.text1.SelectionChanged += SelectionChangedEventHandler(self.select_item)
        # self.button_object.Click += RoutedEventHandler(self.button_run)

        self.ShowDialog()

    def button_run(self, sender, e):
        self.text_results1 = self.text_block1.Text
        self.text_results2 = self.text_block2.Text
        self.Close()
