from Autodesk.Revit import DB

from DoorNWindowSchedule.Enumerations import CodeskTextNoteType
from imports.document import doc, Fec
from searchElement import string_search_get_element_type_by_class_name
from unitConvert import mm2ft


def get_text_not_type():
    """get the sample text note type as a default type"""
    default_text_note_type = Fec(doc).OfClass(DB.TextNoteType).WhereElementIsElementType().FirstElement()

    """"create a list for final collection"""
    text_not_types_list = {}

    def set_type(type_name, text_size=2.0, bolded=False,
                 show_border=False,
                 background=1,
                 font_name="Comic Sans MS",
                 border_offset=0.0):
        text_not_type = string_search_get_element_type_by_class_name(search_name=type_name)

        if text_not_type is None:
            text_not_type = default_text_note_type.Duplicate(type_name)

            text_not_type.LookupParameter("Background").Set(background)
            text_not_type.LookupParameter("Text Size").Set(mm2ft(text_size))
            text_not_type.LookupParameter("Text Font").Set(font_name)
            text_not_type.LookupParameter("Bold").Set(bolded)
            text_not_type.LookupParameter("Show Border").Set(show_border)
            text_not_type.LookupParameter("Leader/Border Offset").Set(border_offset)

            # text_not_type.LookupParameter("Color").Set("Comic Sans MS")

            # print "created text note"

        text_not_types_list.update({type_name: text_not_type})

        "Text note available"
        return text_not_type

    set_type(CodeskTextNoteType.schedule_title, text_size=3, bolded=True)
    set_type(CodeskTextNoteType.schedule_header, text_size=2.5, bolded=True)
    set_type(CodeskTextNoteType.schedule_values, text_size=2.5, bolded=False)
    set_type(CodeskTextNoteType.schedule_small_text, text_size=1.5, bolded=True)

    return text_not_types_list
