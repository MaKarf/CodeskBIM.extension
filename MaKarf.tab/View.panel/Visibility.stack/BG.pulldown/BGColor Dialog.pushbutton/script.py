from Autodesk.Revit.UI import ColorSelectionDialog

app = __revit__.Application


cl = ColorSelectionDialog()
cl.Show()
selected_color = cl.SelectedColor
# print(selected_color)
app.BackgroundColor = selected_color

