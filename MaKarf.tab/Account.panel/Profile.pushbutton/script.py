import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

clr.AddReference('PresentationCore')
clr.AddReference('PresentationFramework')

from System.Windows import Window


class MyWpfWindow(Window):

    def __init__(self):
        self.Title = "My WPF Window"
        self.Width = 400
        self.Height = 200
        self.Content = "Hello, Revit!"


# Create and show the WPF window
wpf_window = MyWpfWindow()
wpf_window.Show()