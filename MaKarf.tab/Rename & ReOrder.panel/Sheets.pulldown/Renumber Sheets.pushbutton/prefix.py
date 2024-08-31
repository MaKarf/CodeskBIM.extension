from Autodesk.Revit.DB import Transaction, ViewSheet
from pyrevit import forms

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Renumber Sheets")


class MyWindow(forms.WPFWindow):
    """GUI for View renaming tool."""

    def __init__(self, xaml_file_name):
        self.form = forms.WPFWindow.__init__(self, xaml_file_name)
        self.alphabets_only = False
        self.selected_items = []

    def __iter__(self):
        """Return selected items."""
        return iter(self.selected_items)

    # >>>>>>>>>> PROPERTIES
    @property
    def prefix(self):
        return self.field_prefix.Text

    @property
    def start_count(self):
        return int(self.field_start_count.Text)

    def check_alphabets_checkbox(self, sender, e):
        self.alphabets_only = True
        return self.alphabets_only

    def uncheck_alphabets_checkbox(self, sender, e):
        self.alphabets_only = False
        return self.alphabets_only

    # >>>>>>>>>> GUI EVENTS
    def buttonclick_run(self, sender, e):
        """Button action: Rename view with given """
        """get collection of sheets selected on the UI forms"""
        ui_selected = ui_doc.Selection.GetElementIds()

        sheets = [doc.GetElement(sheet_id) for sheet_id in ui_selected if
                  type(doc.GetElement(sheet_id)) == ViewSheet]

        self.selected_items = [{"sheets": sheets,
                                "start_number": self.start_count,
                                "prefix": self.prefix,
                                "alphabets_only": self.alphabets_only}]

        self.Close()
