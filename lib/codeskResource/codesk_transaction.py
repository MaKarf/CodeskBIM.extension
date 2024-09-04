import contextlib
import sys
import traceback

from Autodesk.Revit.DB import Transaction


@contextcontextmanager
def try_except(debug=False):
    """ContextManager for Try/Except statement with debug option for except.
    :param debug: if True - Exception error will be displayed with traceback.format_exc()"""
    try:
        yield
    except Exception as e:
        if debug:
            print("*" * 20)
            print("Exception occured: " + traceback.format_exc())
            print("*" * 20)


@contextcontextmanager
def codesk_transaction(doc, title, debug=True, exitscript=False):
    t = Transaction(doc, title)
    t.Start()

    try:
        yield
        t.Commit()

    except Exception as e:
        if debug:
            print("*" * 20)
            print("Exception occured - Transaction is being Rollbacked!")
            print(traceback.format_exc())
            print("*" * 20)
        t.RollBack()

        if exitscript:
            print('*Script Excution stopped!*')
            sys.exit()
