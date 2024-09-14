import sys

from Autodesk.Revit.DB import BuiltInCategory as Bic, Transaction, ViewType
from Autodesk.Revit.DB import FilteredElementCollector as Fec

from UI.Popup import Alert
from loadfamilies import load_family

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Change Grid head")
active_view = ui_doc.ActiveView

app = __revit__.Application

try:
    grid = Fec(doc).OfCategory(Bic.OST_Grids).WhereElementIsNotElementType().ToElements()[0]
except ValueError:
    Alert(title="Report", header="No Grid is placed yet", content="Draw at least a grid and retry")
    

class ChangeFamilyTypes:
    grid_head = None
    section_head = None
    section_line = None

    def __init__(self):
        t.Start()
        self.replace_all()
        try:
            sec = [i for i in Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
                   if i.ViewType == ViewType.Section and not i.IsTemplate][0]
            # for y in sec:
            #     print(y.Name)
            param = doc.GetElement(sec.GetTypeId()).LookupParameter("Section Tag").Element.LookupParameter(
                "Section Tag").AsValueString()
            # print(param)
        except:
            pass
        t.Commit()

    def grids(self):
        try:
            gh = Fec(doc).OfCategory(Bic.OST_GridHeads).WhereElementIsElementType().ToElements()
            self.grid_head = [i for i in gh if "MK_" in i.LookupParameter("Family Name").AsString()][0]
            doc.GetElement(grid.GetTypeId()).LookupParameter("Symbol").Set(self.grid_head.Id)
        except:
            pass

    def sections(self):
        try:
            sh = Fec(doc).OfCategory(Bic.OST_SectionHeads).WhereElementIsElementType().ToElements()
            self.section_head = [i for i in sh if "MK_" in i.LookupParameter("Family Name").AsString()][0]
            param = doc.GetElement(grid.GetTypeId()).LookupParameter("Section Tag").Element.LookupParameter(
                "Section Tag")
            print(param)
        except:
            pass
            # doc. .Set(self.grid_head.Id)

    def replace_all(self):
        self.grids()
        self.sections()

    def replace_families(self):
        try:
            self.grids()
            # self.replace_all()
        except IndexError:
            """ load families and change the grid heads if the families were not loaded already"""
            # load_family()
            """reload the filtered element collector"""
            self.grids()
            # self.replace_all()


ChangeFamilyTypes()
