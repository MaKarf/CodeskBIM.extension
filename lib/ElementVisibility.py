from Autodesk.Revit.DB import FilteredElementCollector, BoundingBoxIntersectsFilter, Outline

doc = __revit__.ActiveUIDocument.Document


def is_visible_in_view(element, view):
    """Get the bounding box of the element"""
    element_bounding_box = element.get_BoundingBox(view)

    if element_bounding_box:
        """Get the bounding box of the view"""
        view_bounding_box = view.CropBox

        """Check if the element's bounding box intersects with the view's bounding box"""
        outline = Outline(element_bounding_box.Min, element_bounding_box.Max)
        element_filter = BoundingBoxIntersectsFilter(outline)
        collector = FilteredElementCollector(doc, view.Id).WherePasses(element_filter)

        if collector.ToElements():
            # print("Element is visible in the view.")
            return True
        else:
            # print("Element is not visible in the view.")
            return False
    else:
        # print("Element does not have a valid bounding box in the view.")
        return None
