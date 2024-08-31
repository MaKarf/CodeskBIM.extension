from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction

import clr

from lib.UI.Popup import Alert
from lib.UI.xamlFiles.CheckboxSelection import CheckboxSelection


clr.AddReference("System")
from System.Windows import Visibility

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Revit Transaction")


rooms = Fec(doc).OfCategory(Bic.OST_Rooms).WhereElementIsNotElementType().ToElementIds()

if len(rooms) != 0:
    item = [{"name": doc.GetElement(room).LookupParameter("Name").AsString(), "element": room} for room in rooms]

    ui = CheckboxSelection(item)

    """hide the error text label if not in used"""
    ui.top_error_message.Visibility = Visibility.Collapsed
    ui.bottom_error_message.Visibility = Visibility.Collapsed
    ui.ShowDialog()

    selected_rooms = ui.selected_items
    if len(selected_rooms) != 0:

        with Transaction(doc, "Delete Rooms") as tx:
            tx.Start()

            for i in rooms:
                doc.Delete(i)
            tx.Commit()


else:
    Alert(title="Notification", header="No Rooms found in the Project", content="")

