# -*- coding: utf-8 -*-
import base64
import os

# codeskbimpyrevitlicpath = r"C:\Windows\codesk\agbodzahlic.py"
codeskbimpyrevitlicpath = r"lib\codeskbimpyrevitlicpath.py"


def byte_images(file, byte_variable):
    pic = open(file, 'rb')
    content = '{} = {}\n'.format(byte_variable, base64.b64encode(pic.read()))
    pic.close()

    with open(codeskbimpyrevitlicpath, 'w') as f:
        f.write(content)
        f.close()


if __name__ == '__main__':
    byte_images('Codesk-logo.png', 'codeskbimpyrevitlic_codesklogo')
    # print("")
