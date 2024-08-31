# import sys
#
# from Autodesk.Revit import DB
# from Autodesk.Revit.DB import BuiltInCategory as Bic, ElementId
# from Autodesk.Revit.DB import FilteredElementCollector as Fec
# from Autodesk.Revit.DB import Transaction
# from Autodesk.Revit.DB import ViewType
# from Autodesk.Revit.Exceptions import ArgumentException
# from System.Collections.Generic import List
#
# from lib.UI.Popup import Alert
# from lib.UI.xamlFiles.CheckboxSelection import CheckboxSelection
#
# ui_doc = __revit__.ActiveUIDocument
# doc = __revit__.ActiveUIDocument.Document
# t = Transaction(doc, "Place Elevations on sheet")
#
#
# def select_views(view_type):
#     view_list = [view for view in Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
#                  if view.ViewType == view_type and not view.IsTemplate]
#
#     ui_data = [{"name": v.Name, "element": v} for v in view_list]
#
#     ui = CheckboxSelection(items=ui_data)
#     ui.ShowDialog()
#
#     return ui.selected_items
#
#
# def select_title_blocks():
#     view_list = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()
#     ui_data = [{"name": tb.Name, "element": tb} for tb in view_list]
#     ui = CheckboxSelection(items=ui_data)
#     ui.ShowDialog()
#     return ui.selected_items
#
#
# def place_elevations_on_sheet():
#     """ collect  and filter out only the elevation views from revit database"""
#     view_list = [view.Id for view in Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
#                  if view.ViewType == ViewType.Elevation and not view.IsTemplate]
#
#     # print(view_list)
#
#     sheets = [s.Id for s in Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements() if
#               "ELEVATION" in s.Name.upper()]
#
#     sheet_ids = List[ElementId](sheets)
#
#     elem_dicts = []
#     for i in sheets:
#         ind = sheets.index(i)
#         sheet_el = doc.GetElement(i)
#         # print("\n========================================================")
#         de = sheet_el.GetDependentElements(None)
#         fam_instance = [fi for fi in de if type(doc.GetElement(fi)) == DB.FamilyInstance and doc.GetElement(
#             fi).Category.Name == "Title Blocks"]
#
#         """ exceptions"""
#         if len(fam_instance) < 1:
#             print("No Title Block found on sheet", i.LookupParameter("Sheet Number").AsValueString())
#             Alert("Resolve by placing a Title Block on the Sheet",
#                   header="Sheet {} has NO Title Block".format(sheet_el.LookupParameter("Sheet Number").AsValueString()))
#             sys.exit()
#         elif len(fam_instance) > 1:
#             """use only one if title blocks on the view sheet is more than one """
#             print("Multiple Title Block found on sheet", i.LookupParameter("Sheet Number").AsValueString())
#             Alert("Only ONE Title Block is needed on a Sheet",
#                   header="Sheet {} has MULTIPLE Title Block".format(
#                       sheet_el.LookupParameter("Sheet Number").AsValueString()))
#             # elem_dicts.append({"sheet_id": sheet_ids[ind], "title_block": fam_instance[0]})
#             sys.exit()
#
#         elif len(fam_instance) == 1:
#             tt_block = doc.GetElement(fam_instance[0])
#             # print(tt_block)
#             bb = tt_block.get_BoundingBox(sheet_el)
#             # print(bb)
#             elem_dicts.append({"sheet_id": sheet_ids[ind], "title_block": tt_block, "tt_bbox": bb})
#
#     t.Start()
#     try:
#         for elem in elem_dicts:
#             bbox = elem.get("tt_bbox")
#             titleBlock_Min = bbox.Min
#             titleBlock_Max = bbox.Max
#
#             title_block_height = titleBlock_Max.Y - titleBlock_Min.Y
#             title_block_width = titleBlock_Max.X - titleBlock_Min.X
#
#             index = elem_dicts.index(elem)
#             if len(sheets) == 4:
#                 # print(elem)
#
#                 """place view starting from the left side of the title block"""
#                 viewport_location = DB.XYZ(bbox.Min.X + title_block_width * 0.5, bbox.Min.Y + title_block_height * 0.5,
#                                            0)
#                 DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[index], viewport_location)
#
#             elif len(sheets) == 2:
#                 viewport_location1 = DB.XYZ(bbox.Min.X + title_block_width * 0.5,
#                                             bbox.Min.Y + title_block_height * 0.25, 0)
#                 viewport_location2 = DB.XYZ(bbox.Min.X + title_block_width * 0.5,
#                                             bbox.Min.Y + title_block_height * 0.75, 0)
#                 if index == 0:
#
#                     DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[0], viewport_location1)
#                     DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[1], viewport_location2)
#
#                 else:
#                     DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[2], viewport_location1)
#                     DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[3], viewport_location2)
#
#             elif len(sheets) == 1:
#                 viewport_location1 = DB.XYZ(bbox.Min.X + title_block_width * 0.25,
#                                             bbox.Min.Y + title_block_height * 0.25, 0)
#                 viewport_location2 = DB.XYZ(bbox.Min.X + title_block_width * 0.25,
#                                             bbox.Min.Y + title_block_height * 0.75, 0)
#                 viewport_location3 = DB.XYZ(bbox.Min.X + title_block_width * 0.75,
#                                             bbox.Min.Y + title_block_height * 0.25, 0)
#                 viewport_location4 = DB.XYZ(bbox.Min.X + title_block_width * 0.75,
#                                             bbox.Min.Y + title_block_height * 0.75, 0)
#
#                 DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[0], viewport_location1)
#                 DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[1], viewport_location2)
#                 DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[2], viewport_location3)
#                 DB.Viewport.Create(doc, elem.get("sheet_id"), view_list[3], viewport_location4)
#
#             else:
#                 Alert(header="Elevations sheets are not 2 or 4")
#                 t.RollBack()
#                 sys.exit()
#
#     except ArgumentException:
#         Alert(header="Views Already Placed on Sheets")
#
#     except IndexError:
#         Alert(title="Error", content="Rectify and Retry", header="Some Elevation(s) might be deleted")
#
#     t.Commit()
#
#
# # place_elevations_on_sheet()
#
# m = select_views(ViewType.Elevation)
# if m is not None:
#     print(m)
#
#     n = select_title_blocks()
#     if n is not None:
#         print(n)
import clr

from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from lib.UI.xamlFiles.forms import ListItem

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")

from System.Collections.Generic import List
from System.Windows.Controls import SelectionChangedEventHandler, TextBlock
from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler

from Autodesk.Revit import DB

from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView
t = DB.Transaction(doc, "Load Site Plan")


class PlaceViewsOnSheets(BaseWPFClass):

    def __init__(self, views_data=None, sheets_data=None):
        BaseWPFClass.__init__(self, xaml_file_name="PlaceViewsOnSheets.xaml")

        self.views_data = views_data
        self.sheets_data = sheets_data

        """Find the "button_run" button by its name"""
        self.view_type_filter = self.Window.FindName("view_type_filter")
        self.report_selected = self.Window.FindName("report_selected")

        self.views_list_box_panel = self.Window.FindName("views_list_box_panel")
        self.views_list_box = self.Window.FindName("views_list_box")

        self.sheets_list_box_panel = self.Window.FindName("sheets_list_box_panel")
        self.sheets_list_box = self.Window.FindName("sheets_list_box")

        self.views_selector = self.Window.FindName("views_selector")
        self.sheets_selector = self.Window.FindName("sheets_selector")

        self.search = self.Window.FindName("search")
        self.button_run = self.Window.FindName("button_run")

        self.select_all = self.Window.FindName("select_all")
        self.select_none = self.Window.FindName("select_none")

        self.run_button = self.Window.FindName("run_button")

        """Attach the event handler to the button's "Click" event"""
        self.views_selector.Checked += RoutedEventHandler(self.select_views)
        self.views_selector.Unchecked += RoutedEventHandler(self.select_views)

        self.sheets_selector.Checked += RoutedEventHandler(self.select_sheets)
        self.sheets_selector.Unchecked += RoutedEventHandler(self.select_sheets)

        self.run_button.Click += RoutedEventHandler(self.run)

        self.focused_width = (self.Window.Width - 50) * 0.7
        self.unfocused_width = (self.Window.Width - 50) * 0.3

        self.views_selector.IsChecked = True

        """set items sources"""
        self.views_combobox_data = self.generate_list_items(self.views_data)
        self.views_list_box.ItemsSource = self.views_combobox_data

        self.sheets_combobox_data = self.generate_list_items(sheets_data)
        self.sheets_list_box.ItemsSource = self.sheets_combobox_data

        self.search.KeyUp += KeyEventHandler(self.search_filter)
        self.view_type_filter.SelectionChanged += SelectionChangedEventHandler(self.filter_by_view_type)

    def generate_list_items(self, data_items):
        list_of_items = List[type(ListItem(cls=self))]()

        if data_items is not None:
            for item in data_items:
                list_of_items.Add(ListItem(cls=self, name=item.get("name"), element=item.get("element"),
                                           select_multiple=True))
            return list_of_items
        return None

    def select_views(self, sender, e):
        if self.views_selector.IsChecked:

            self.sheets_selector.IsChecked = False
            self.views_list_box_panel.Width = self.focused_width
            self.sheets_list_box_panel.Width = self.unfocused_width
        else:
            self.sheets_selector.IsChecked = True
            self.views_list_box_panel.Width = self.unfocused_width
            self.sheets_list_box_panel.Width = self.focused_width

    def select_sheets(self, sender, e):
        if self.sheets_selector.IsChecked:
            self.views_selector.IsChecked = False
            self.views_list_box_panel.Width = self.unfocused_width
            self.sheets_list_box_panel.Width = self.focused_width
        else:
            self.views_selector.IsChecked = True
            self.views_list_box_panel.Width = self.focused_width
            self.sheets_list_box_panel.Width = self.unfocused_width

    def search_filter(self, sender, e):
        # if sender.Text.replace(" ", "").isdigit()
        pass

    def filter_by_view_type(self):
        pass

    def run(self, sender, e):
        # if not self.lock:
        self.Close()


"""how to use the class"""
if __name__ == "__main__":
    view_list = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
    sheet_list = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()

    # for i in view_list:
    #     print "SHEET NAME",  i.Name

    views = [{"name": i.Name, "element": i} for i in view_list]
    sheets = [{"name": i.Name, "element": i} for i in sheet_list]

    # item1 = [{"name": "ItemOne {}".format(i), "element": i} for i in range(20)]
    # item2 = [{"name": "ItemTwo {}".format(i), "element": i} for i in range(20)]
    ui = PlaceViewsOnSheets(views, sheets).ShowDialog()
