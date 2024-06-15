import PyQt5.QtWidgets as pqw
from PyQt5 import uic
import os
import sys
import dataHandler
import patient_manager
import record_items
import screen_manager


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class PatientRecordUI(pqw.QMainWindow):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    def __init__(self):
        super(PatientRecordUI, self).__init__()
        self.ui = resource_path("resources/assets/ui/patient_records.ui")
        uic.loadUi(self.ui, self)

        self.patient_phone_number = patient_manager.patient_list[
            screen_manager.widget.widget(0).patient_list_widget.currentRow()].get_info("phone_number")
        self.record_selected = False

        self.findChild(pqw.QAction, "actionShow_Patients").triggered.connect(self.get_main_window)

        self.patient_records_list_widget = self.findChild(pqw.QListWidget, "patient_records_list_widget")
        self.patient_records_list_widget.clicked.connect(self.select_record)
        self.patient_records_list_widget.itemDoubleClicked.connect(self.open_record)

        self.open_record_button = self.findChild(pqw.QPushButton, "open_record_button")
        self.open_record_button.clicked.connect(self.open_record)

        self.add_new_record_button = self.findChild(pqw.QPushButton, "add_new_record_button")
        self.add_new_record_button.clicked.connect(self.add_new_record)

        # self.show_records()

    def get_main_window(self):
        import screen_manager
        screen_manager.show_screen("MainWindow")

    def show_records(self):
        self.patient_phone_number = [v.rstrip().lstrip() for v in
                                     screen_manager.widget.widget(0).patient_list_widget.currentItem().text().split(
                                         "|")][-1]
        self.patient_records_list_widget.clear()
        last_visited_dates = [dates for dates in
                              eval(dataHandler.query_patient_info("last_visited_date", self.patient_phone_number))]
        for date in last_visited_dates:
            self.patient_records_list_widget.addItem(date)

    def select_record(self):
        self.record_selected = True

    def open_record(self):
        patient = dataHandler.fetch_patient(self.patient_phone_number)
        if self.record_selected:
            date = self.patient_records_list_widget.currentItem().text()
            date_index = eval(dataHandler.query_patient_info("last_visited_date", self.patient_phone_number)).index(
                date)
            screen_manager.show_screen("PatientInfoUI")
            # print(screen_manager.widget.widgetscreen_manager.widget.widget(0).findChild(pqw.QPushButton, "add_new_record_button").text())
            # print(screen_manager.widget.currentIndex())
            screen_manager.widget.currentWidget().show_existing_record(patient, date, date_index)

    def add_new_record(self):
        patient = dataHandler.fetch_patient(self.patient_phone_number)
        screen_manager.show_screen("PatientInfoUI")
        screen_manager.widget.currentWidget().add_new_record_screen(patient)
