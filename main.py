import PyQt5.QtWidgets as pqw
from PyQt5 import uic
import os
import sys
import patient_manager
import dataHandler


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UI(pqw.QMainWindow):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    def __init__(self):
        super(UI, self).__init__()
        self.ui = resource_path("resources/assets/ui/main_window.ui")
        # load ui
        uic.loadUi(self.ui, self)
        self.patient_selected = False
        dataHandler.create_database()
        self.show_patient_list(patient_manager.patient_list)

        self.patient_list_widget = self.findChild(pqw.QListWidget, "patient_list_widget")
        self.patient_list_widget.clicked.connect(self.select_patient)
        self.patient_list_widget.itemDoubleClicked.connect(self.go_to_patient_record_screen)

        self.view_patient_button = self.findChild(pqw.QPushButton, "view_patient_button")
        self.view_patient_button.clicked.connect(self.go_to_patient_record_screen)

        self.create_new_patient = self.findChild(pqw.QAction, "actionCreate_New_Patient")
        self.create_new_patient.triggered.connect(self.new_patient_screen)

        self.delete_patient_action = self.findChild(pqw.QAction, "actionDelete_Patient")
        self.delete_patient_action.triggered.connect(self.delete_patient)

        self.search_bar = self.findChild(pqw.QLineEdit, "search_textbox")
        self.search_bar.returnPressed.connect(self.search_patients)
        self.search_button = self.findChild(pqw.QPushButton, "search_button")
        self.search_button.clicked.connect(self.search_patients)

        self.clear_search_button = self.findChild(pqw.QPushButton, "clear_search_button")
        self.clear_search_button.clicked.connect(self.clear_search)

    def go_to_patient_record_screen(self):
        self.patient_selected = False
        screen_manager.show_screen("PatientRecordUI")

    def select_patient(self):
        self.patient_selected = True

    def new_patient_screen(self):
        screen_manager.show_screen("PatientInfoUI")
        screen_manager.widget.currentWidget().show_new_patient_screen()

    def show_patient_list(self, patient_list):
        for patient in patient_list:
            self.patient_list_widget.addItem(f'{patient.get_info("name")} | {patient.get_info("phone_number")}')

    def search_patients(self):
        if self.search_bar.text() != "":
            matched_patients = [patients for patients in patient_manager.patient_list if
                                self.search_bar.text().lower() == patients.get_info(
                                    "name").lower() or self.search_bar.text() == patients.get_info("phone_number")]
            self.patient_list_widget.clear()
            self.show_patient_list(matched_patients)
        else:
            self.patient_list_widget.clear()
            self.show_patient_list(patient_manager.patient_list)

    def clear_search(self):
        self.patient_list_widget.clear()
        self.search_bar.setText("")
        self.show_patient_list(patient_manager.patient_list)

    def delete_patient(self):
        if self.patient_selected:
            sure = input(f"are you sure you want to delete {self.patient_list_widget.currentItem().text()} : ")
            if sure == "y":
                dataHandler.delete_patient(
                    patient_manager.patient_list[self.patient_list_widget.currentRow()].get_info("phone_number"))
                patient_manager.update_patient_list()
                self.patient_list_widget.clear()
                self.show_patient_list(patient_manager.patient_list)


App = pqw.QApplication(sys.argv)
mainWindow = UI()
import screen_manager

screen_manager.widget.addWidget(mainWindow)
screen_manager.widget.setFixedSize(551, 453)
screen_manager.widget.show()
UI_WINDOW = UI()
App.exec_()
