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
