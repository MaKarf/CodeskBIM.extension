from Autodesk.Revit import DB

from Autodesk.Revit.DB import DatumEnds, Transaction

from UI.Popup import Alert
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from selection.ui_selection import rectangular_selection_by_category

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Grid Bubble")
active_view = ui_doc.ActiveView


class HideGridBubble(BaseWPFClass):
    grids = rectangular_selection_by_category(DB.BuiltInCategory.OST_Grids)
    top_or_right_bubble = DatumEnds.End0
    bottom_or_left_bubble = DatumEnds.End1

    def __init__(self):
        if self.grids:
            BaseWPFClass.__init__(self, xaml_file_name="HideGridBubble.xaml")
            self.ShowDialog()
        else:
            Alert(title="No Grids found", header="No Grids found", content="Place Grid and retry")
            self.close_window()

    def hide_bubble(self, datum_end):
        for grid in self.grids:
            grid.HideBubbleInView(datum_end, active_view)

    def show_bubble(self, datum_end):
        for grid in self.grids:
            grid.ShowBubbleInView(datum_end, active_view)

    def checked(self, sender, e):
        t.Start()
        """start checkbox clicked"""
        if sender.Name == "check_object_start":
            if sender.IsChecked:
                self.show_bubble(self.bottom_or_left_bubble)
            else:
                self.hide_bubble(self.bottom_or_left_bubble)

        else:
            if sender.IsChecked:
                self.show_bubble(self.top_or_right_bubble)
            else:
                self.hide_bubble(self.top_or_right_bubble)
        t.Commit()

    def ui_button_run(self, sender=None, event=None):
        self.Close()


HideGridBubble()
