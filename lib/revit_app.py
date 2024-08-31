from Autodesk.Revit.UI import UIApplication

if __name__ == "__main__":
    __revit__ = UIApplication


app = __revit__.Application

ui_app = UIApplication(app)

ui_doc = __revit__.ActiveUIDocument

doc = ui_doc.Document

# active