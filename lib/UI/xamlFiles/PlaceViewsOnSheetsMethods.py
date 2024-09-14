from Autodesk.Revit import DB
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic
from Autodesk.Revit.DB import Transaction

from SortNatural import real_sorting
from unitConvert import mm2ft

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Place Elevations on sheet")


class SelectedViewsAndTBlocks:

    def __init__(self, ui_class_ref):

        self.lock = ui_class_ref.lock

        if not self.lock:
            self.selected_views = ui_class_ref.selected_views
            self.selected_sheets = ui_class_ref.selected_sheets
            self.sheet = self.selected_sheets.pop()
            self.array_type = ui_class_ref.placement_array

            dependants = self.sheet.GetDependentElements(None)

            title_block = [doc.GetElement(i) for i in dependants if type(doc.GetElement(i)) == DB.FamilyInstance and
                           doc.GetElement(i).Category.Name == "Title Blocks"].pop()
            self.tt_bb = title_block.get_BoundingBox(self.sheet)

            self.title_block_height = self.tt_bb.Max.Y - self.tt_bb.Min.Y
            self.title_block_width = self.tt_bb.Max.X - self.tt_bb.Min.X

            """process"""
            num_of_views = len(self.selected_views)

            self.title_block_x_pos = self.tt_bb.Min.X
            self.title_block_allowable_width = self.title_block_width * 0.75
            self.horizontal_limit = self.title_block_x_pos + self.title_block_allowable_width

            self.viewport_allocated_width = self.title_block_allowable_width / num_of_views
            self.viewport_allocated_height = self.title_block_height / num_of_views

    @staticmethod
    def get_views_by_type(view_type):
        vl = [view for view in Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
              if view.ViewType == view_type and not view.IsTemplate and view.Name]

        list_to_sort = [{"name": str(v.Name), "element": v, } for v in vl if v is not None]
        res = real_sorting(list_to_be_sorted=list_to_sort,
                           dict_key="name")
        return res

    def horizontal_array(self):
        for view in self.selected_views:
            counter = self.selected_views.index(view)

            horizontal_offset = mm2ft(10)
            half_viewport_x_offset = self.viewport_allocated_width / 2

            viewport_x_pos = self.title_block_x_pos + (
                    counter * self.viewport_allocated_width) + half_viewport_x_offset + horizontal_offset

            viewport_y_pos = self.title_block_height / 2

            viewport_location = DB.XYZ(viewport_x_pos, viewport_y_pos, 0)

            DB.Viewport.Create(doc, self.sheet.Id, view.Id, viewport_location)

    def vertical_array(self):
        for view in self.selected_views:
            counter = self.selected_views.index(view)
            title_block_y_pos = self.tt_bb.Min.Y
            vertical_offset = mm2ft(10)
            half_viewport_y_offset = self.viewport_allocated_height / 2

            viewport_x_pos = self.title_block_width / 2
            viewport_y_pos = title_block_y_pos + (
                    counter * self.viewport_allocated_height) + half_viewport_y_offset + vertical_offset

            viewport_location = DB.XYZ(viewport_x_pos, viewport_y_pos, 0)

            DB.Viewport.Create(doc, self.sheet.Id, view.Id, viewport_location)

    def place_views(self):
        if not self.lock:
            t.Start()
            if self.array_type == "horizontal":
                self.horizontal_array()
            else:
                self.vertical_array()
            t.Commit()


# SelectedViewsAndTBlocks().place_views()
