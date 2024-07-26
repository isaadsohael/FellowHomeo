import PyQt5.QtWidgets as pqw
from PyQt5 import uic
from services import dataHandler, screen_manager, resource_path, constants


class PatientRecordUI(pqw.QMainWindow):

    def __init__(self):
        super(PatientRecordUI, self).__init__()

        # main screen ui declaration
        self.ui = resource_path.resource_path(constants.patient_record_screen_dir)

        # load ui
        uic.loadUi(self.ui, self)

        self.record_selected = False
        self.last_visited_dates = []

        self.findChild(pqw.QAction, constants.actionShow_Patients).triggered.connect(
            lambda x: screen_manager.show_screen("MainWindow"))

        self.patient_records_list_widget = self.findChild(pqw.QListWidget, constants.patient_records_list_widget)
        self.patient_records_list_widget.clicked.connect(self.select_record)
        self.patient_records_list_widget.itemDoubleClicked.connect(self.open_record)

        self.open_record_button = self.findChild(pqw.QPushButton, constants.open_record_button)
        self.open_record_button.clicked.connect(self.open_record)

        self.add_new_record_button = self.findChild(pqw.QPushButton, constants.add_new_record_button)
        self.add_new_record_button.clicked.connect(self.add_new_record)

        self.findChild(pqw.QAction, constants.actionQuit).triggered.connect(
            lambda x: screen_manager.show_dialog("Confirm QUIT", "Are you sure you want to close the app?",
                                                 do_what="quit"))

        self.patient_name = self.findChild(pqw.QLabel, constants.name)
        self.patient_phone_number = self.findChild(pqw.QLabel, constants.phone_number)
        self.record_sort_button = self.findChild(pqw.QComboBox, constants.record_sort_button)
        self.record_sort_button.currentTextChanged.connect(self.sort_patient_record)

    def show_records(self, show_record_of):
        try:
            self.patient_name.setText(dataHandler.query_patient_info("name", show_record_of))
            self.patient_phone_number.setText(dataHandler.query_patient_info("phone_number", show_record_of))
        except:
            self.patient_name.setText("PatientName")
            self.patient_phone_number.setText("PatientPhoneNumber")

        self.last_visited_dates = [dates for dates in
                                   eval(dataHandler.query_patient_info("last_visited_date", show_record_of))]
        self.last_visited_dates.sort(reverse=True)  # sort newest to oldest (larger to smaller)

        self.add_records_to_screen()

    def add_records_to_screen(self):
        self.patient_records_list_widget.clear()
        for date in self.last_visited_dates:
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

    def sort_patient_record(self):
        if self.record_sort_button.currentText() == constants.sort_oldest:
            self.last_visited_dates.sort()
            self.add_records_to_screen()

        if self.record_sort_button.currentText() == constants.sort_newest:
            self.last_visited_dates.sort(reverse=True)
            self.add_records_to_screen()
