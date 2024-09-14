from Autodesk.Revit.DB import Transaction
from update_projects_data import ProjectData

from lib.UI.UIData import generate_data_from_dict
from lib.UI.xamlFiles.DropDownSelection import DropDownSelection
from lib.UI.XamlComponent import load_xaml_from_string, Visibility

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Load Grids")
active_view = ui_doc.ActiveView

"""Your XAML string"""
xaml_string = '''
<StackPanel xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
            xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"             
             
             Orientation="Vertical"             
             Margin="0"
             Height="70">
             
    <StackPanel>
        <Button x:Name="expansion_button_checkbox" 
        Content="..." 
        FontWeight="Heavy" 
        Background="Transparent"
        Foreground="Red"
        Width="80" />
        
    </StackPanel>
    
    <StackPanel>
        <Button
            Margin="0,20,0,0"
            x:Name="delete_button"
            Content="Delete Option"
            Height="20"
            FontSize="11"    
            VerticalAlignment="Center"            
            HorizontalAlignment="Center"/>    
    </StackPanel>
    
</StackPanel>
'''


class LoadGrids(DropDownSelection):
    pd = ProjectData(doc.Title)

    def __init__(self, title=None, label_name=None, dropdown_list=None, button_name=None,
                 show_window_automatically=False):

        DropDownSelection.__init__(self, title, label_name, dropdown_list, button_name,
                                   show_window_automatically=show_window_automatically)

        self.Height = 140
        """Load the StackPanel from the XAML string"""
        self.stack_layout = load_xaml_from_string(xaml_string)

        """Find the button and bind the event"""

        self.expansion_button_checkbox = self.stack_layout.FindName("expansion_button_checkbox")
        self.expansion_button_checkbox.Click += self.toggle_expansion_panel

        self.delete_button = self.stack_layout.FindName("delete_button")
        self.delete_button.Width = self.Width
        self.delete_button.Click += self.delete_option_click

        self.bottom_allowance_panel.Children.Add(self.stack_layout)
        self.delete_button.Visibility = Visibility.Collapsed

        self.ShowDialog()

    def toggle_expansion_panel(self, sender, event_args):

        if self.delete_button.Visibility == Visibility.Visible:
            self.delete_button.Visibility = Visibility.Collapsed
            self.Height -= 20
        else:
            self.delete_button.Visibility = Visibility.Visible
            self.Height += 20

    def delete_option_click(self, sender, event_args):
        """Define the event handler for the Delete button click"""
        # print len(self.dropdown_dict_data)
        if len(self.dropdown_dict_data) != 0:
            # print "UPDATED LIST"
            """delete from database"""
            data = self.pd.delete_grid_option(self.selected_item.Name)
            updated_dropdown_list = generate_data_from_dict(data)
            #
            self.update_selection(updated_dropdown_list)

            if not self.dropdown_object.ItemsSource:
                self.delete_button.Visibility = Visibility.Collapsed
                self.bottom_allowance_panel.Visibility = Visibility.Collapsed
                self.Height -= 30
                self.exited_with_close_button = True
                self.button_object.Content = "Close"

