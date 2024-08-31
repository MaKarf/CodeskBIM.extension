import clr

from System.Collections.Generic import List

clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System.Windows import RoutedEventHandler
from System.Windows import Thickness
from System.Windows.Controls import StackPanel, Orientation, CheckBox


class ListItem(StackPanel):
    """Helper Class for displaying selected sheets in my custom GUI."""

    def __init__(self, cls, name='', element=None, select_multiple=True, *args):
        super(ListItem, self).__init__(*args)

        """Attach the event handler to the button's "Click" event"""
        self.cls = cls
        self.element = element
        self.select_multiple = select_multiple

        """Attach the event handler to the button's "Click" event"""
        self.Orientation = Orientation.Horizontal
        self.Margin = Thickness(0, 0, 0, 0)

        """Attach the event handler to the button's "Click" event"""
        self.check_box = CheckBox()
        self.check_box.Content = name

        try:
            self.check_box.Tag = "{}_{}".format(name, element.Id.IntegerValue)
        except AttributeError:
            pass

        self.check_box.Checked += RoutedEventHandler(self.checkbox_checked)
        self.check_box.Unchecked += RoutedEventHandler(self.checkbox_checked)
        self.Children.Add(self.check_box)

    def checkbox_checked(self, sender, e):
        self.cls.checker(sender)


def generate_list_items(self):
    list_of_items = List[type(ListItem(cls=self))]()

    if self.dict_items is not None:
        for item in self.dict_items:
            list_of_items.Add(ListItem(cls=self, name=item.get("name"), element=item.get("element"),
                                       select_multiple=self.select_multiple))
        return list_of_items
    return None
