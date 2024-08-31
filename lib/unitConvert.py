from Autodesk.Revit.DB import UnitUtils

app = __revit__.Application
rvt_year = int(app.VersionNumber)


def ft2mm(digit):
    if str(type(digit)) == "<type 'XYZ'>":
        res = (round(float(digit[0]) / 0.003281),
               round(float(digit[1]) / 0.003281),
               round(float(digit[2]) / 0.003281))
        # print(res)
        return res
    elif str(type(digit)) == "<type 'float'>":
        res = round(float(digit) / 0.003281)
        # print(res)
        return res

    elif str(type(digit)) == "<type 'int'>":
        res = int(round(float(digit) / 0.003281))
        # print(res)
        return res


def mm2ft(digit):
    if str(type(digit)) == "<type 'XYZ'>":
        res = (round((float(digit[0]) * 0.003281), 5),
               round((float(digit[1]) * 0.003281), 5),
               round((float(digit[2]) * 0.003281), 5))
        # print(res)
        return res
    elif str(type(digit)) == "<type 'float'>":
        res = round((float(digit) * 0.003281), 5)
        # print(res)
        return res

    elif str(type(digit)) == "<type 'int'>":
        res = round((float(digit) * 0.003281), 5)
        # print(res)
        return res


def convert_mm_to_feet(length):
    """Function to convert cm to feet."""

    # RVT >= 2022
    if rvt_year < 2022:
        from Autodesk.Revit.DB import DisplayUnitType
        return UnitUtils.Convert(length, DisplayUnitType.DUT_MILLIMETERS, DisplayUnitType.DUT_DECIMAL_FEET)
    # RVT >= 2022
    else:
        from Autodesk.Revit.DB import UnitTypeId
        return UnitUtils.ConvertToInternalUnits(length, UnitTypeId.Millimeters)


def convert_cm_to_feet(length):
    """Function to convert cm to feet."""

    # RVT >= 2022
    if rvt_year < 2022:
        from Autodesk.Revit.DB import DisplayUnitType
        return UnitUtils.Convert(length, DisplayUnitType.DUT_CENTIMETERS, DisplayUnitType.DUT_DECIMAL_FEET)
    # RVT >= 2022
    else:
        from Autodesk.Revit.DB import UnitTypeId
        return UnitUtils.ConvertToInternalUnits(length, UnitTypeId.Centimeters)


def convert_m_to_feet(length):
    """Function to convert cm to feet."""

    # RVT >= 2022
    if rvt_year < 2022:
        from Autodesk.Revit.DB import DisplayUnitType
        return UnitUtils.Convert(length, DisplayUnitType.DUT_METERS, DisplayUnitType.DUT_DECIMAL_FEET)
    # RVT >= 2022
    else:
        from Autodesk.Revit.DB import UnitTypeId
        return UnitUtils.ConvertToInternalUnits(length, UnitTypeId.Meters)


def convert_internal_to_m(length):
    """Function to convert internal to meters."""

    # RVT >= 2022
    if rvt_year < 2022:
        from Autodesk.Revit.DB import DisplayUnitType
        return UnitUtils.Convert(length, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
    # RVT >= 2022
    else:
        from Autodesk.Revit.DB import UnitTypeId
        return UnitUtils.ConvertFromInternalUnits(length, UnitTypeId.Meters)


def convert_internal_to_cm(length):
    """Function to convert internal to centimeters."""

    # RVT >= 2022
    if rvt_year < 2022:
        from Autodesk.Revit.DB import DisplayUnitType
        return UnitUtils.Convert(length, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_CENTIMETERS)
    # RVT >= 2022
    else:
        from Autodesk.Revit.DB import UnitTypeId
        return UnitUtils.ConvertFromInternalUnits(length, UnitTypeId.Centimeters)


def convert_internal_to_m2(area):
    """Function to convert internal to meters."""

    # RVT >= 2022
    if rvt_year < 2022:
        from Autodesk.Revit.DB import DisplayUnitType
        return UnitUtils.Convert(area, DisplayUnitType.DUT_SQUARE_FEET, DisplayUnitType.DUT_SQUARE_METERS)
    # RVT >= 2022
    else:
        from Autodesk.Revit.DB import UnitTypeId
        return UnitUtils.ConvertFromInternalUnits(area, UnitTypeId.SquareMeters)
