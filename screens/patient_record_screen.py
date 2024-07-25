import PyQt5.QtWidgets as pqw
from PyQt5 import uic
from services import dataHandler, screen_manager, resource_path


class PatientRecordUI(pqw.QMainWindow):

    def __init__(self):
        super(PatientRecordUI, self).__init__()

        # main screen ui declaration
        self.ui = resource_path.resource_path("resources/assets/ui/patient_records.ui")

        # load ui
        uic.loadUi(self.ui, self)

        self.record_selected = False

        self.findChild(pqw.QAction, "actionShow_Patients").triggered.connect(self.get_main_window)

        self.patient_records_list_widget = self.findChild(pqw.QListWidget, "patient_records_list_widget")
        self.patient_records_list_widget.clicked.connect(self.select_record)
        self.patient_records_list_widget.itemDoubleClicked.connect(self.open_record)

        self.open_record_button = self.findChild(pqw.QPushButton, "open_record_button")
        self.open_record_button.clicked.connect(self.open_record)

        self.add_new_record_button = self.findChild(pqw.QPushButton, "add_new_record_button")
        self.add_new_record_button.clicked.connect(self.add_new_record)

        self.findChild(pqw.QAction, "actionQuit").triggered.connect(
            lambda x: screen_manager.show_dialog("Confirm QUIT", "Are you sure you want to close the app?",
                                                 do_what="quit"))

        self.patient_name = self.findChild(pqw.QLabel, "name")
        self.patient_phone_number = self.findChild(pqw.QLabel, "phone_number")

    def get_main_window(self):
        screen_manager.show_screen("MainWindow")

    def show_records(self, show_record_of):
        try:
            self.patient_name.setText(dataHandler.query_patient_info("name", show_record_of))
            self.patient_phone_number.setText(dataHandler.query_patient_info("phone_number", show_record_of))
        except:
            self.patient_name.setText("PatientName")
            self.patient_phone_number.setText("PatientPhoneNumber")

        self.patient_records_list_widget.clear()
        last_visited_dates = [dates for dates in
                              eval(dataHandler.query_patient_info("last_visited_date", show_record_of))]
        for date in last_visited_dates:
            self.patient_records_list_widget.addItem(date)

        self.record_selected = False

    def select_record(self):
        self.record_selected = True

    def open_record(self):

        patient = dataHandler.fetch_patient(self.patient_phone_number.text())
        if self.record_selected:
            date = self.patient_records_list_widget.currentItem().text()
            screen_manager.show_screen("PatientInfoUI", show_record_of=self.patient_phone_number.text())
            screen_manager.widget.currentWidget().show_existing_record(patient, date)

    def add_new_record(self):
        patient = dataHandler.fetch_patient(self.patient_phone_number.text())
        screen_manager.show_screen("PatientInfoUI", show_record_of=self.patient_phone_number.text())
        screen_manager.widget.currentWidget().add_new_record_screen(patient)
