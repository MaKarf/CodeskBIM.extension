from UI.xamlFiles.Grids.Rename.RenameGridsUI import RenameGridsUI
from UI.xamlFiles.Grids.Selection import SelectGrids


class RenameGrids(SelectGrids):

    def __init__(self, selection_type, include_hidden_grids=None, list_of_grids=None):
        SelectGrids.__init__(self, selection_type, include_hidden_grids=include_hidden_grids, list_of_grids=list_of_grids)

        if not self.exited_with_close_button:
            RenameGridsUI(self, include_hidden_grids=include_hidden_grids)
