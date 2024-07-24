import PyQt5.QtWidgets as pqw
import sys
import os
import dataHandler

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

dataHandler.create_database()
App = pqw.QApplication(sys.argv)

import main_screen
import screen_manager

mainWindow = main_screen.UI()
screen_manager.widget.addWidget(mainWindow)
screen_manager.widget.show()
App.exec_()
