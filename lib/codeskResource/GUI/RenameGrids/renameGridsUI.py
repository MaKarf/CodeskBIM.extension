from pyrevit import forms


class RenameGridsUIClass(forms.WPFWindow):
    def __init__(self, rename_class=None):
        self.form = forms.WPFWindow.__init__(self, "renameGridsUI.xaml")
        self.rename_class = rename_class
        """UPDATE GUI ELEMENTS"""
        self.ShowDialog()

    def reverse_horizontal(self, sender, e):
        self.rename_class.reverse_h_grids(self.numeric_grid_prefix.Text)

    def inverse_horizontal(self, sender, e):
        self.rename_class.inverse_h_grids(self.numeric_grid_prefix.Text)

    def reverse_vertical(self, sender, e):
        self.rename_class.reverse_v_grids(self.alphabetic_grid_prefix.Text)

    def inverse_vertical(self, sender, e):
        self.rename_class.inverse_v_grids(self.alphabetic_grid_prefix.Text)

    def reverse_swap_names(self, sender, e):
        self.rename_class.reverse_swap_names()

    def swap_grid_names(self, sender, e):
        self.rename_class.swap_grid_names()

    def rename(self, sender, e):
        self.rename_class.rename_grids()

    """reuse the inverse method for assigning prefix to the grids names since those methods do not reverse the order
    of the names but just add prefixes.
    There is n need to add the prefix methods inside the .py UI class. It has been tackled here"""

    def prefix_horizontal(self, sender, e):
        self.inverse_horizontal("a", "b")

    def prefix_vertical(self, sender, e):
        self.inverse_vertical("a", "b")

    def close_button(self, sender, e):
        self.Close()
