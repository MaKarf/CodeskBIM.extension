import operator

from getView import EnableRevealHiddenElements, DisableRevealHiddenElements, get2DView
from imports.DotNetSystem import List
from selection.ui_selection import rectangular_selection_by_category

from .CommonImports import doc, Fec, Bic, ui_doc, t, active_view, Color, DB, SelectionType
from .Load.LoadGrids import LoadGrids
from ...Popup import Alert
from ...UIData import generate_data_from_dict

# view2d = get2DView()
view2d = active_view


# print view2d.Name


class SelectGrids:
    exited_with_close_button = False
    excluded_grids = []

    horizontal_grids = []
    vertical_grids = []
    vertical_and_horizontal_grids = []
    merged_vertical_and_horizontal_grids = []

    def __init__(self, selection_type, include_hidden_grids=None, list_of_grids=None):
        self.all_grids_from_revit_db = Fec(doc).OfCategory(Bic.OST_Grids).WhereElementIsNotElementType().ToElements()

        self.__elem_ids = List[DB.ElementId]()
        self.__all_grids_collection = None
        self.__only_visible_grids_collection = None

        if selection_type == SelectionType.select_from_db:
            self.from_revit_db(include_hidden_grids)

        elif selection_type == SelectionType.select_from_ui:
            self.from_revit_ui()

        elif selection_type == SelectionType.select_from_list:
            self.from_list(list_of_grids)

        else:
            self.from_saved_options()

    def from_revit_db(self, include_hidden_grids=None):
        """i want to avoid constant querying of the db anytime the include hidden grids are toggles
        which will slow down the process.
         I want to save the query in a temp variable when the this method is called for the first time"""
        # \
        #     if self.__all_grids_collection is None else self.__all_grids_collection
        #
        # """update the temp var"""
        # if self.__all_grids_collection is None:
        #     self.__all_grids_collection = main_grids_collection

        if include_hidden_grids is True:
            main_grids_collection = self.all_grids_from_revit_db
            # self.excluded_grids = []

            # print len(main_grids_collection)

        else:
            # print "mk"

            # main_grids_collection = [i for i in main_grids_collection if i.get_BoundingBox(get2DView())] \
            #     if self.__only_visible_grids_collection is None else self.__only_visible_grids_collection
            main_grids_collection = [i for i in self.all_grids_from_revit_db if i.get_BoundingBox(view2d)]
            # print len(main_grids_collection)
        # print "SELECT FROM DB: {} grids  | {}".format(len(main_grids_collection),
        #                                               [g.Name for g in main_grids_collection])

        # """update the temp var"""
        # if self.__only_visible_grids_collection is None:
        #     self.__only_visible_grids_collection = main_grids_collection

        sub_grids_collection = []

        return self.__final_ordered_grids(main_grids_collection, sub_grids_collection)

    def from_revit_ui(self):
        temp_main_grids = self.__select_grids_from_ui(Color(247, 191, 158))
        sub_grids_collection = self.__select_grids_from_ui(Color(5, 5, 5))

        main_grids_collection = list(filter(lambda x: x.Id not in [i.Id for i in sub_grids_collection],
                                            temp_main_grids
                                            )
                                     )
        return self.__final_ordered_grids(main_grids_collection, sub_grids_collection)

    def from_saved_options(self):
        return self.__transform_data()

    def from_list(self, list_of_grids):
        main_grids_collection = list_of_grids
        sub_grids_collection = []
        return self.__final_ordered_grids(main_grids_collection, sub_grids_collection)

    "_______________________________________________________________________________________________________"
    "__________________________________ PRIVATE METHODS ____________________________________________________"
    "_______________________________________________________________________________________________________"

    def set_excluded_grids(self, all_selected_grids):
        self.excluded_grids = [{"name": i.Name, "elem": i} for i in self.all_grids_from_revit_db if
                               i not in [j["elem"] for j in all_selected_grids]]

        # print "Len of All_grids: {}".format(len(self.all_grids_from_revit_db))
        # print "Len of selected_grids: {}".format(len(all_selected_grids))
        # print "Len of excluded_grids: {}".format(len(self.excluded_grids))

    def __final_ordered_grids(self, main_grids_collection, sub_grids_collection):

        main_grids_as_dict_data = self.__convert_to_dict_data(main_grids_collection, is_sub_grid=False)
        sub_grids_as_dict_data = self.__convert_to_dict_data(sub_grids_collection, is_sub_grid=True)

        all_grids_as_dict_data = main_grids_as_dict_data + sub_grids_as_dict_data
        self.set_excluded_grids(all_grids_as_dict_data)

        # print("\n\n"
        #       "original main {}\n"
        #       "converted main: {}\n"
        #       "converted sub: {}\n\n".format(
        #     [g.Name for g in main_grids_collection],
        #     [g["elem"].Name for g in main_grids_as_dict_data],
        #     [g["elem"].Name for g in sub_grids_as_dict_data]))

        # print "__FINAL ORDER: {} grids  | {}".format(
        #     len(all_grids_as_dict_data),
        #     [g["elem"].Name for g in all_grids_as_dict_data])

        grids = self.__ordered_by_orientation(all_grids_as_dict_data)
        return grids

    @staticmethod
    def __convert_to_dict_data(raw_grids_collection, is_sub_grid=False):
        grids_collection_list = []
        if len(raw_grids_collection) == 0:
            return []
        else:

            t.Start()
            EnableRevealHiddenElements(active_view)

            for grid in raw_grids_collection:

                """open the reveal hidden element to get the bounding box of the hidden grids"""

                """get viewports placed on sheet"""

                b_box = grid.get_BoundingBox(active_view)
                grid_length = b_box.Max.X - b_box.Min.X
                grid_height = b_box.Max.Y - b_box.Min.Y

                if grid_length > grid_height:
                    orientation = "horizontal"
                    origin = b_box.Max.Y - (grid_height / 2)
                else:
                    orientation = "vertical"
                    origin = b_box.Max.X - (grid_length / 2)

                grids_collection_list.append(
                    {"elem": grid, "name": grid.Name, "orientation": orientation, "origin": origin,
                     "sub": is_sub_grid})

            DisableRevealHiddenElements(view2d)
            t.Commit()

            return grids_collection_list

    def __ordered_by_orientation(self, grids_as_dict_data):
        horizontal_grids = []
        vertical_grids = []
        for g in grids_as_dict_data:
            if g.get("orientation") == "horizontal":
                horizontal_grids.append(g)
            else:
                vertical_grids.append(g)

        ordered_vertical_grids = sorted(vertical_grids, key=operator.itemgetter("origin"), reverse=False)
        ordered_horizontal_grids = sorted(horizontal_grids, key=operator.itemgetter("origin"), reverse=True)

        self.vertical_and_horizontal_grids = [ordered_horizontal_grids, ordered_vertical_grids]

        # print "\n\nself.vertical_grids: {}\n\nself.horizontal_grids: {}\n\n".format(ordered_vertical_grids,
        #                                                                             ordered_horizontal_grids)

        """update class variables for global access"""
        self.horizontal_grids = ordered_horizontal_grids
        self.vertical_grids = ordered_vertical_grids
        self.merged_vertical_and_horizontal_grids = self.horizontal_grids + self.vertical_grids

        # print "ORDER BY ORIENTATION: {} grids  | {}".format(len(self.merged_vertical_and_horizontal_grids),
        #                                                     [g["elem"].Name for g in
        #                                                      self.merged_vertical_and_horizontal_grids])

        return self.vertical_and_horizontal_grids

    @staticmethod
    def __select_grids_from_ui(bg_color):
        try:
            """grids category = -2000220"""
            grids_collection = rectangular_selection_by_category(
                built_in_category=DB.BuiltInCategory.OST_Grids,
                as_elements=True,
                temp_bg_color=bg_color)

            return grids_collection
        except Exception:
            Alert("", header="No Grid was selected")
            return None

    def __transform_data(self):
        from lib.update_projects_data import ProjectData

        pd = ProjectData(doc.Title)
        data = pd.active_project_data_dict["grids_selection_options"]
        # print data
        if data:
            dict_data = generate_data_from_dict(data)
            # print "Data: {}".format(dict_data)

            """pop up CompoBox UI and select an option"""
            ui = LoadGrids(dropdown_list=dict_data)
            if ui.selected_item is not None:
                selected = ui.selected_item.Value
                self.exited_with_close_button = ui.exited_with_close_button

                main_grids_collection = self.__get_elements_from_ids(selected["main_grids"])
                sub_grids_collection = self.__get_elements_from_ids(selected["sub_grids"])

                ui_doc.Selection.SetElementIds(self.__elem_ids)

                return self.__final_ordered_grids(main_grids_collection, sub_grids_collection)
        else:
            # print "no data"
            Alert(title="No Grid option saved", header="No Grid option saved", content="No data to display")
            return None

    def __get_elements_from_ids(self, list_of_ids):
        """find revit elements with the selected ids"""
        if list_of_ids:

            elem_ids = List[DB.ElementId]()

            grid_elements = List[DB.Element]()

            [elem_ids.Add(DB.ElementId(int(ids))) for ids in list_of_ids if
             doc.GetElement(DB.ElementId(int(ids))) is not None]

            [grid_elements.Add(doc.GetElement(i)) for i in elem_ids if doc.GetElement(i) is not None]

            self.__elem_ids.AddRange(elem_ids)
            return grid_elements
        else:
            return []

# horizontal_and_vertical_grids = SelectGrids().from_revit_db()
# horizontal_and_vertical_grids = SelectGrids().from_saved_options()
# horizontal_and_vertical_grids = SelectGrids().from_revit_ui()
