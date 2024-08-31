def run_as_admin():
    import os
    import sys
    import win32com.shell.shell as shell
    as_admin = 'asadmin'

    if sys.argv[-1] != as_admin:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [as_admin])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        # sys.exit(0)

    # import ctypes
    #
    # import subprocess
    # import sys
    #
    # if not ctypes.windll.shell32.IsUserAnAdmin():
    #     print("not an admin, restarting...")
    #     subprocess.run(["launcher.exe", sys.executable, *sys.argv])
    # else:
    #     print("I'm an admin now.")


if __name__ == "__main__":
    run_as_admin()
