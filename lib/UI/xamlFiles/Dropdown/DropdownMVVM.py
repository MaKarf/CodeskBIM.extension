import clr

clr.AddReference("PresentationFramework")
clr.AddReference("WindowsBase")
clr.AddReference("System")
clr.AddReference("System.ComponentModel")

from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventHandler, PropertyChangedEventArgs
from System.Collections.ObjectModel import ObservableCollection
from System.Windows import Application, Window
from System.Windows.Controls import ComboBox, StackPanel


class YourModel(INotifyPropertyChanged):
    """Implementing INotifyPropertyChanged in IronPython"""
    def __init__(self, property_name):
        self._property_name = property_name
        self.PropertyChanged = None

    @property
    def PropertyName(self):
        return self._property_name

    @PropertyName.setter
    def PropertyName(self, value):
        if self._property_name != value:
            self._property_name = value
            self.OnPropertyChanged("PropertyName")

    def OnPropertyChanged(self, property_name):
        if self.PropertyChanged:
            self.PropertyChanged(self, PropertyChangedEventArgs(property_name))


class ViewModel(INotifyPropertyChanged):
    """ViewModel with ObservableCollection"""
    def __init__(self):
        self.Items = ObservableCollection[YourModel]()
        self.Items.Add(YourModel("Item 1"))
        self.Items.Add(YourModel("Item 2"))

    # No need for INotifyPropertyChanged here unless the ViewModel has other properties you want to notify on.


class MyWindow(Window):
    """Main Window Setup"""
    def __init__(self):
        self.Title = "IronPython WPF ComboBox"
        self.Width = 300
        self.Height = 200

        # Create ViewModel
        self.DataContext = ViewModel()

        # Create UI Elements
        panel = StackPanel()
        self.Content = panel

        # Create ComboBox and bind to ItemsSource
        combo_box = ComboBox()
        combo_box.ItemsSource = self.DataContext.Items
        combo_box.DisplayMemberPath = "PropertyName"

        # Add ComboBox to StackPanel
        panel.Children.Add(combo_box)


# Initialize and run the WPF application
if __name__ == '__main__':
    app = Application()
    window = MyWindow()
    app.Run(window)
