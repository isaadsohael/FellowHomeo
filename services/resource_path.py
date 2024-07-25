"""
Why use this file? Read Below...
- https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/#dealing-with-relative-paths:~:text=icons%2C%20keep%20reading!-,Dealing%20with%20relative%20paths,-There%20is%20a
- https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
"""

import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    return os.path.join(base_path, relative_path)
