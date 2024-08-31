from lib.selection.ui_selection import hide_selection
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Transaction, ElementId, Color
from Autodesk.Revit.Exceptions import OperationCanceledException
from System.Collections.Generic import List

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Hide Elements")

"""note down the current background color before selection"""
bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)

"""get elements in selection before the button was clicked"""
ui_selection = ui_doc.Selection.GetElementIds()
try:
    """ display revit selection wizard if nothing was selected before the button was clicked"""
    if len(ui_selection) == 0:
        """change the background color to indicate user to select elements"""
        app.BackgroundColor = Color(247, 191, 158)

        element_ids = List[ElementId]()

        selected_references = ui_doc.Selection.PickObjects(ObjectType.Element)
        selected_items = [element_ids.Add(doc.GetElement(ref).Id) for ref in selected_references]
        """ reset background color after selection"""
        app.BackgroundColor = bg_color

        """exit if nothing was still selected"""
        if len(selected_items) > 0:
            t.Start()
            """hide elements"""
            hide_selection(element_ids)
            t.Commit()
    else:
        t.Start()
        hide_selection(ui_selection)
        t.Commit()

    """ exit if command is cancelled"""
except OperationCanceledException:
    app.BackgroundColor = bg_color
