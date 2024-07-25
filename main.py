import PyQt5.QtWidgets as pqw
import sys
import os
from services import dataHandler

# https://stackoverflow.com/questions/64686336/when-i-try-to-run-my-pyqt5-app-the-windows-sizes-changing
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

dataHandler.create_database()
App = pqw.QApplication(sys.argv)

from screens import main_screen
from services import screen_manager

mainWindow = main_screen.UI()
screen_manager.widget.addWidget(mainWindow)
screen_manager.widget.show()
App.exec_()
