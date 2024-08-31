# -*- coding: utf-8 -*-
import os

from Autodesk.Revit.DB import Color

app = __revit__.Application


def prepare_directory(self):
    path = r"C:\ProgramData\Autodesk\Codesk\Makarf Add-in\docs"
    try:
        if self.path_file_name in os.listdir(path):
            self.default_project_folder = open(self.full_path, "r").read()
    except:
        os.makedirs(path)
        with open(self.full_path, "w") as pt:
            pt.write(self.default_project_folder)
            pt.close()


def bg_color():
    path = r"C:\ProgramData\Autodesk\Codesk\Makarf Add-in\docs"
    favourite_bg_colours_file_name = "favourite_bg_colours_path.txt"
    favourite_bg_colours_path = r"{}\{}".format(path, favourite_bg_colours_file_name)

    """ list of favourite colour to be added to colour list"""
    a = Color(255, 255, 255)
    b = Color(190, 190, 190)
    c = Color(241, 210, 173)
    d = Color(247, 191, 158)
    e = Color(143, 110, 90)
    f = Color(50, 50, 50)
    g = Color(33, 40, 50)
    h = Color(58, 68, 83)
    i = Color(69, 84, 110)

    bg = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)

    """ add favourite colour choices to the colour list"""
    color_list = [a, b, c, d, e, f, g, h, i]

    """#########################################################################################################"""
    """#########################################################################################################"""

    """ saving the colours in on the local machine"""
    # try:
    #     if favourite_bg_colours_file_name in os.listdir(path):
    #         color_list = open(favourite_bg_colours_path, "r").read()
    #         for v in color_list:
    #             print(v)
    # except:
    #     os.makedirs(path)
    #     with open(favourite_bg_colours_path, "w") as pt:
    #         for colo in color_list:
    #             pt.write(colo)
    #             pt.close()
    """#########################################################################################################"""
    """#########################################################################################################"""

    """ cater for current background colours that are not in the list"""
    feedback_bool = []
    for c in color_list:
        if bg.Red == c.Red and bg.Blue == c.Blue and bg.Green == c.Green:
            feedback_bool.append(True)
        else:
            feedback_bool.append(False)

    if True in feedback_bool:
        pass
    else:
        color_list.append(bg)

    """get the current background colour in revit workspace"""
    current_color = app.BackgroundColor
    for colour in color_list:
        # print(colour.Red, colour.Green, colour.Blue)
        """ if current background color is equal to the colour found in the list
        jump to the next colour using base of the index of the current colour in the list"""
        if current_color.Red == colour.Red and current_color.Blue == colour.Blue and current_color.Green == colour.Green:
            next_color_index = color_list.index(colour) + 1

            """if the colors get to the last item switch the index to the 1st color in the list to continue the cycle"""
            if next_color_index > len(color_list) - 1:
                next_color_index = 0
                app.BackgroundColor = color_list[next_color_index]
            else:
                app.BackgroundColor = color_list[next_color_index]


def run():
    bg_color()
