import os
import sys

from rpw.ui.forms import Alert


def individual_lic(test_func):
    try:
        from codeskResource.medicine.global_access import global_access, variable_name
        # print(len(variable_name))
        if global_access and len(variable_name) == 3338908:
            # print("Access Granted")
            test_func()
        else:
            Alert("You do not have license to use this button",
                  title="License Error",
                  header="Access Denied")

    except ImportError:
        Alert("This Button is not accessible at the moment",
              title="Import Error | No drugs found",
              header="Access Denied")
        sys.exit()

    except NameError:
        Alert("This Button is not accessible at the moment",
              title="Name Error",
              header="Access Denied")
        sys.exit()

    # def secondary_lic_check():
    #     p = r"C:\Program Files\pyRevit-Master\extensions\CodeskBIM.extension\lib\codeskResource\startup.exe"
    #     pt = "010000110011101001011100010100000111001001101111011001110111001001100001011011010010000001000110011010010110110001100101011100110101110001110000011110010101001001100101011101100110100101110100001011010100110101100001011100110111010001100101011100100101110001100101011110000111010001100101011011100111001101101001011011110110111001110011010111000100001101101111011001000110010101110011011010110100001001001001010011010010111001100101011110000111010001100101011011100111001101101001011011110110111001011100011011000110100101100010010111000110001101101111011001000110010101110011011010110101001001100101011100110110111101110101011100100110001101100101010111000111001101110100011000010111001001110100011101010111000000101110011001010111100001100101"
    #     p2 = r"D:\8.myGitHub\Git-Revit\Python4Revit\CodeskBIMpyRevit"
    #     cd_p = 'CodeskBIM.extension'
    #     ex = "lib\\codeskResource\\startup.exe"
    #     path = os.path.join(p2, cd_p, ex)
    #     return path
    #
    # """ check for lic on every button click everytime"""
    # os.startfile(secondary_lic_check())

    """########################################################################################################"""
    """########################################################################################################"""
