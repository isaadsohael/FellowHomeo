import sys
import PyQt5.QtWidgets as pqw
from PyQt5 import uic
import os
import patient_manager
import record_items
import dataHandler
import screen_manager


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class PatientInfoUI(pqw.QMainWindow):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    def __init__(self):
        super(PatientInfoUI, self).__init__()
        self.ui = resource_path("resources/assets/ui/patient_info.ui")
        uic.loadUi(self.ui, self)
        self.edit_record_button = self.findChild(pqw.QPushButton, "edit_record_button")

        self.add_delete_record_button = self.findChild(pqw.QPushButton, "add_delete_record_button")
        self.add_delete_record_button.clicked.connect(self.add_delete_patient_record)

        self.add_new_patient_action = self.findChild(pqw.QAction, "actionAdd_New_Patient")
        self.add_new_patient_action.setEnabled(True)
        self.add_new_patient_action.triggered.connect(self.show_new_patient_screen)

        self.findChild(pqw.QAction, "actionShow_Patients").triggered.connect(self.get_main_window)
        self.findChild(pqw.QAction, "actionGo_Back").triggered.connect(self.go_back)

        self.patient_phone_number = self.findChild(pqw.QPlainTextEdit, "phone_number")

        self.edit_record_button.setEnabled(True)
        self.edit_record_button.setHidden(False)
        self.add_delete_record_button.setHidden(False)
        self.show_new_patient_screen()

    def get_main_window(self):
        self.clear_textbox()
        import screen_manager
        screen_manager.show_screen("MainWindow")

    def go_back(self):
        self.clear_textbox()
        if self.add_new_patient_action.isEnabled():
            screen_manager.show_screen("PatientRecordUI")
        else:
            screen_manager.show_screen("MainWindow")

    def show_new_patient_screen(self):
        self.add_delete_record_button.setText("Add Record")
        for item in record_items.patient_record_items:
            self.findChild(pqw.QPlainTextEdit, item).setPlainText("")
            self.findChild(pqw.QPlainTextEdit, item).setEnabled(True)

        self.edit_record_button.setEnabled(False)
        self.edit_record_button.setHidden(False)
        self.add_delete_record_button.setHidden(False)
        self.findChild(pqw.QAction, "actionAdd_New_Patient").setEnabled(False)

    def show_existing_record(self, patient, date, date_index):
        self.add_new_patient_action.setEnabled(True)
        self.add_delete_record_button.setText("Delete Record")
        for item in record_items.patient_record_items:
            if item != "date" and item != "last_visited_date":
                if item not in record_items.variable_records:
                    record = patient[record_items.patient_record_items.index(item)]
                    self.findChild(pqw.QPlainTextEdit, item).setPlainText(record)
                    self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)
                else:
                    record = eval(patient[record_items.patient_record_items.index(item)])[date_index]
                    self.findChild(pqw.QPlainTextEdit, item).setPlainText(record)
                    self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)
            elif item == "last_visited_date":
                record = eval(patient[record_items.patient_record_items.index(item)])[-1]
                self.findChild(pqw.QPlainTextEdit, item).setPlainText(record)
                self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)
            else:
                self.findChild(pqw.QPlainTextEdit, item).setPlainText(date)
                self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)

    def add_new_record_screen(self, patient):
        patient_info = []
        self.edit_record_button.setEnabled(False)
        self.add_delete_record_button.setText("Add New Record")
        for item in record_items.patient_record_items:
            if item != "date":
                if item not in record_items.variable_records:
                    record = patient[record_items.patient_record_items.index(item)]
                    self.findChild(pqw.QPlainTextEdit, item).setPlainText(record)
                    self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)
                    patient_info.append(record)
                else:
                    if item == "last_visited_date":
                        last_visited_date = eval(dataHandler.query_patient_info("last_visited_date", patient_info[
                            record_items.patient_record_items.index("phone_number")]))[-1]
                        self.findChild(pqw.QPlainTextEdit, item).setPlainText(last_visited_date)
                        self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)

    def add_delete_patient_record(self):
        patient_info = []
        if self.add_delete_record_button.text() == "Add Record":
            if not patient_manager.patient_exists(self.patient_phone_number.toPlainText()):
                # patient does not exist
                for item in record_items.patient_record_items:
                    if item not in record_items.variable_records:
                        record = self.findChild(pqw.QPlainTextEdit, item).toPlainText()
                        patient_info.append(record)
                    else:
                        # creating this format ['last_visited_date']
                        if item == "last_visited_date":
                            record = [self.findChild(pqw.QPlainTextEdit, "date").toPlainText()]
                            patient_info.append(str(record))
                        else:
                            record = [self.findChild(pqw.QPlainTextEdit, item).toPlainText()]
                            patient_info.append(str(record))

                dataHandler.add_patient(patient_info)
                patient_manager.update_patient_list()
                print("patient added successfully")

            else:
                # patient exists
                # TODO: do stuff if  patient already exists: warning - 1) go to update record screen or - 2) change record
                print("patient exists")

        elif self.add_delete_record_button.text() == "Add New Record":
            for item in record_items.patient_record_items:
                if item not in record_items.variable_records:
                    record = self.findChild(pqw.QPlainTextEdit, item).toPlainText()
                    patient_info.append(record)
                else:
                    if item == "last_visited_date":
                        last_visited_dates = [dates for dates in
                                              eval(dataHandler.query_patient_info("last_visited_date",
                                                                                  patient_info[
                                                                                      record_items.patient_record_items.index(
                                                                                          "phone_number")]))]
                        record = last_visited_dates + [self.findChild(pqw.QPlainTextEdit, "date").toPlainText()]
                        patient_info.append(str(record))
                    else:
                        prev_record = eval(dataHandler.query_patient_info(item, patient_info[
                            record_items.patient_record_items.index("phone_number")]))
                        record = prev_record + [self.findChild(pqw.QPlainTextEdit, item).toPlainText()]
                        patient_info.append(str(record))
            dataHandler.update_patient(patient_info[record_items.patient_record_items.index("phone_number")],
                                       patient_info)
            patient_manager.update_patient_list()
            print("new record added successfully")

        else:
            record_date = self.findChild(pqw.QPlainTextEdit, "date").toPlainText()
            sure = input(f"Are you sure you want to delete {record_date}: ")
            if sure == 'y':
                self.delete_record(record_date)
                screen_manager.show_screen("PatientRecordUI")

    def clear_textbox(self):
        for item in record_items.patient_record_items:
            self.findChild(pqw.QPlainTextEdit, item).setEnabled(True)
            self.findChild(pqw.QPlainTextEdit, item).clear()
        self.add_delete_record_button.setEnabled(True)
        self.edit_record_button.setEnabled(True)

    def delete_record(self, record_date):
        patient_info = list(dataHandler.fetch_patient(self.findChild(pqw.QPlainTextEdit, "phone_number").toPlainText()))
        record_date_index = eval(patient_info[record_items.patient_record_items.index("last_visited_date")]).index(
            record_date)
        for item in record_items.variable_records:
            record = eval(patient_info[record_items.patient_record_items.index(item)])
            record.remove(record[record_date_index])
            patient_info[record_items.patient_record_items.index(item)] = str(record)
        dataHandler.update_patient(self.findChild(pqw.QPlainTextEdit, "phone_number").toPlainText(), patient_info)
