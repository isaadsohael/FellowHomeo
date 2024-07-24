import shutil
import sys
import PyQt5.QtWidgets as pqw
from PyQt5 import uic
import os

import constants
import patient_manager
import screen_manager
import record_items
import dataHandler


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)


class PatientInfoUI(pqw.QMainWindow):

    def __init__(self):
        super(PatientInfoUI, self).__init__()

        # patient info screen ui declaration
        self.ui = resource_path("resources/assets/ui/patient_info.ui")

        # load ui
        uic.loadUi(self.ui, self)

        self.patient_phone_number = ""
        self.patient_records = []
        self.changed_record = {}
        self.opened_record_date = ""
        self.selected_image_directory = []
        self.selected_video_directory = []
        self.images_destination_directory = ""
        self.videos_destination_directory = ""

        self.form_has_information = False

        self.edit_record_button = self.findChild(pqw.QPushButton, "edit_record_button")
        self.edit_record_button.clicked.connect(self.edit_patient_record)

        self.add_delete_record_button = self.findChild(pqw.QPushButton, "add_delete_record_button")
        self.add_delete_record_button.clicked.connect(self.add_delete_patient_record)

        self.add_new_patient_action = self.findChild(pqw.QAction, "actionAdd_New_Patient")
        self.add_new_patient_action.setEnabled(True)
        self.add_new_patient_action.triggered.connect(self.show_new_patient_screen)

        self.findChild(pqw.QPushButton, "necessary_images").clicked.connect(lambda x: self.select_media("images"))
        self.findChild(pqw.QPushButton, "necessary_videos").clicked.connect(lambda x: self.select_media("videos"))

        self.findChild(pqw.QAction, "actionShow_Patients").triggered.connect(
            lambda x: self.go_back_confirmation("actionShow_Patients"))
        self.findChild(pqw.QAction, "actionGo_Back").triggered.connect(
            lambda x: self.go_back_confirmation("actionGo_Back"))

        self.edit_record_button.setEnabled(True)
        self.show_new_patient_screen()

        self.findChild(pqw.QAction, "actionQuit").triggered.connect(
            lambda x: screen_manager.show_dialog("Confirm QUIT", "Are you sure you want to close the app?",
                                                 do_what="quit"))

    def show_info_of(self, patient_phone_number):
        self.patient_phone_number = patient_phone_number

    def get_main_window(self):
        self.clear_textbox()
        screen_manager.show_screen("MainWindow")

    def go_back_confirmation(self, button_pressed):

        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                if self.findChild(pqw.QPlainTextEdit, item).toPlainText() != "":
                    self.form_has_information = True
            else:
                if self.findChild(pqw.QPushButton, item).text() not in ["Add Images", "Add Videos"]:
                    self.form_has_information = True

        # reference button (ref_btn) helps determine which page we are at (eg: new or exisiting profile page)
        ref_btn = self.findChild(pqw.QPushButton, "add_delete_record_button")
        if ref_btn.text() == "Add Record":
            # going back from new patient profile screen
            if self.form_has_information:
                screen_manager.show_dialog("Warning",
                                           "Are you sure you want to go back?",
                                           detailed_text="Closing this Window will erase all data you have entered in the boxes.",
                                           do_what="go_back_warning")
            else:
                screen_manager.show_screen("MainWindow")

        else:
            # going back from existing patient profile screen
            if ref_btn.text() == "Update Record":  # patient record is/trying to be edited!
                form_updated = False
                i = 0
                for item in record_items.patient_record_items:
                    if item not in record_items.record_buttons:
                        if self.findChild(pqw.QPlainTextEdit, item).toPlainText() != self.patient_records[i]:
                            form_updated = True
                            break
                    else:
                        if self.findChild(pqw.QPushButton, item).text() != self.patient_records[i]:
                            form_updated = True
                            break
                    i += 1
                if form_updated:
                    screen_manager.show_dialog("Warning",
                                               "Are you sure you want to go back?",
                                               detailed_text="Going back will remove any changes to the data that is not saved.",
                                               do_what="go_back_warning")
                else:
                    screen_manager.show_screen("PatientRecordUI",
                                               self.patient_phone_number) if button_pressed == "actionGo_Back" else screen_manager.show_screen(
                        "MainWindow")
            else:  # just visited the record. not on update screen or any other.!
                screen_manager.show_screen("PatientRecordUI",
                                           self.patient_phone_number) if button_pressed == "actionGo_Back" else screen_manager.show_screen(
                    "MainWindow")

    def go_back(self, event):
        if event.text() == "&Yes":
            self.clear_textbox()
            if self.add_new_patient_action.isEnabled():
                screen_manager.show_screen("PatientRecordUI", self.patient_phone_number)
            else:
                screen_manager.show_screen("MainWindow")

            for item in record_items.patient_record_items:
                if item not in record_items.record_buttons:
                    self.findChild(pqw.QPlainTextEdit, item).clear()
                else:
                    if item == "necessary_images":
                        self.findChild(pqw.QPushButton, item).setText("Add Images")
                    else:
                        self.findChild(pqw.QPushButton, item).setText("Add Videos")

    def show_new_patient_screen(self):
        self.findChild(pqw.QLabel, "patient_info_screen_header").setText("Create New Patient Profile")
        self.add_delete_record_button.setText("Add Record")
        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                self.findChild(pqw.QPlainTextEdit, item).setPlainText("")
                self.findChild(pqw.QPlainTextEdit, item).setReadOnly(False)
                self.findChild(pqw.QPlainTextEdit, item).setEnabled(True)
            else:
                self.findChild(pqw.QPushButton, item).setEnabled(True)

        self.edit_record_button.setEnabled(False)
        self.findChild(pqw.QAction, "actionAdd_New_Patient").setEnabled(False)

    def show_existing_record(self, patient_info: tuple, date):
        self.findChild(pqw.QLabel, "patient_info_screen_header").setText(
            f"Patient Record for date {date}")
        self.opened_record_date = date
        self.add_new_patient_action.setEnabled(True)
        self.edit_record_button.setEnabled(True)
        self.add_delete_record_button.setText("Delete Record")
        self.patient_records.clear()

        date_index = eval(dataHandler.query_patient_info("last_visited_date", patient_info[
            record_items.patient_record_items.index("phone_number")])).index(
            date)
        for item in patient_info:
            if patient_info.index(item) == record_items.patient_record_items.index("date"):
                self.patient_records.append(date)
            elif patient_info.index(item) == record_items.patient_record_items.index("last_visited_date"):
                self.patient_records.append(eval(item)[-1])
            else:
                try:
                    self.patient_records.append(eval(item)[date_index])
                except:
                    self.patient_records.append(item)

        i = 0
        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                self.findChild(pqw.QPlainTextEdit, item).setPlainText(self.patient_records[i])
                self.findChild(pqw.QPlainTextEdit, item).setReadOnly(True)
            else:
                self.findChild(pqw.QPushButton, item).setText(self.patient_records[i])
            i += 1

    def add_new_record_screen(self, patient):
        self.add_new_patient_action.setEnabled(True)
        self.edit_record_button.setEnabled(False)
        self.add_delete_record_button.setText("Add New Record")
        patient_info = []

        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                if item != "date":
                    if item not in record_items.variable_records:
                        record = patient[record_items.patient_record_items.index(item)]
                        self.findChild(pqw.QPlainTextEdit, item).setPlainText(record)
                        self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)
                        patient_info.append(record)
                    else:
                        if item == "last_visited_date":
                            last_visited_date = \
                                eval(dataHandler.query_patient_info("last_visited_date", self.patient_phone_number))[-1]
                            self.findChild(pqw.QPlainTextEdit, item).setPlainText(last_visited_date)
                            self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)

    def form_filled(self):
        filled = True
        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                if item != "last_visited_date" and self.findChild(pqw.QPlainTextEdit, item).document().isEmpty():
                    filled = False
            else:
                if self.findChild(pqw.QPushButton, item).text() in ["Add Images", "Add Videos"]:
                    filled = False
        return filled

    def add_delete_patient_record(self):
        patient_info = []

        if self.add_delete_record_button.text() == "Add Record":
            if self.form_filled():
                if not patient_manager.patient_exists(self.findChild(pqw.QPlainTextEdit, "phone_number").toPlainText()):
                    # patient does not exist
                    for item in record_items.patient_record_items:
                        if item not in record_items.variable_records:
                            record = self.findChild(pqw.QPlainTextEdit, item).toPlainText()
                            patient_info.append(record)
                        else:
                            if item not in record_items.record_buttons:
                                # creating this format ['last_visited_date']
                                if item == "last_visited_date":
                                    record = [self.findChild(pqw.QPlainTextEdit, "date").toPlainText()]
                                    patient_info.append(str(record))
                                else:
                                    record = [self.findChild(pqw.QPlainTextEdit, item).toPlainText()]
                                    patient_info.append(str(record))
                            else:
                                record = [self.findChild(pqw.QPushButton, item).text()]
                                patient_info.append(str(record))

                    dataHandler.add_patient(patient_info)
                    self.add_media()
                    patient_manager.update_patient_list()
                    screen_manager.show_dialog("Success", "Patient Added Successfully")
                    self.clear_textbox()
                    self.go_back_confirmation("actionGo_Back")
                else:
                    # patient exists
                    screen_manager.show_dialog("Patient Exists",
                                               f"Patient with phone number {self.findChild(pqw.QPlainTextEdit, 'phone_number').toPlainText()} already exists | Do you want to View Existing Patient?",
                                               detailed_text=f"{self.findChild(pqw.QPlainTextEdit, 'phone_number').toPlainText()} number already exists with Name: {dataHandler.query_patient_info('name', self.findChild(pqw.QPlainTextEdit, 'phone_number').toPlainText())}",
                                               do_what="patient_exists")
            else:
                screen_manager.show_dialog("Warning", "All Form Information should be filled")

        elif self.add_delete_record_button.text() == "Add New Record":
            for item in record_items.patient_record_items:
                if item not in record_items.variable_records:
                    record = self.findChild(pqw.QPlainTextEdit, item).toPlainText()
                    patient_info.append(record)
                else:
                    if item not in record_items.record_buttons:
                        if item == "last_visited_date":
                            last_visited_dates = [dates for dates in
                                                  eval(dataHandler.query_patient_info("last_visited_date",
                                                                                      self.patient_phone_number))]
                            record = last_visited_dates + [self.findChild(pqw.QPlainTextEdit, "date").toPlainText()]
                            patient_info.append(str(record))
                        else:
                            prev_record = eval(dataHandler.query_patient_info(item, self.patient_phone_number))
                            record = prev_record + [self.findChild(pqw.QPlainTextEdit, item).toPlainText()]
                            patient_info.append(str(record))
                    else:
                        prev_record = eval(dataHandler.query_patient_info(item, self.patient_phone_number))
                        record = prev_record + [self.findChild(pqw.QPushButton, item).text()]
                        patient_info.append(str(record))

            dataHandler.update_patient(self.patient_phone_number, patient_info)
            patient_manager.update_patient_list()
            screen_manager.show_dialog("Success", "Patient New Record Added Successfully")
            self.clear_textbox()
            self.go_back_confirmation("actionGo_Back")

        elif self.add_delete_record_button.text() == "Update Record":
            self.check_for_records_to_update()

        elif self.add_delete_record_button.text() == "Delete Record":
            screen_manager.show_dialog("Warning",
                                       f"Are you sure you want to delete the record on {self.opened_record_date}?",
                                       detailed_text=f"All record on the date {self.opened_record_date} for the patient {dataHandler.query_patient_info('name', self.patient_phone_number)} will be deleted from this profile!",
                                       do_what="delete_record")

    def check_for_records_to_update(self):
        updated_records = []
        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                updated_records.append(self.findChild(pqw.QPlainTextEdit, item).toPlainText())
            else:
                updated_records.append(self.findChild(pqw.QPushButton, item).text())
        for v in record_items.patient_record_items:
            index = record_items.patient_record_items.index(v)
            if updated_records[index] != self.patient_records[index]:
                self.changed_record[v] = updated_records[index]

        if "phone_number" in self.changed_record.keys() and patient_manager.patient_exists(
                self.changed_record["phone_number"]):
            # if :
            screen_manager.show_dialog("Warning",
                                       "Phone Number Exists | Do you want to View Existing Patient?",
                                       detailed_text=f"{self.changed_record['phone_number']} number already exists with Name: {dataHandler.query_patient_info('name', self.changed_record['phone_number'])}",
                                       do_what="patient_exists")

        elif "date" in self.changed_record.keys() and self.changed_record['date'] in eval(
                dataHandler.query_patient_info("last_visited_date", self.patient_phone_number)):
            screen_manager.show_dialog("Warning",
                                       "Record Exists | Do you want to View Existing Record?",
                                       detailed_text=f"Record on {self.changed_record['date']} already exists with for this Patient: {dataHandler.query_patient_info('name', self.patient_phone_number)}",
                                       do_what="record_exists")
        else:
            self.update_patient_record()

    def update_patient_record(self):
        patient_info = list(dataHandler.fetch_patient(self.patient_phone_number))
        date = self.patient_records[record_items.patient_record_items.index("date")]
        date_index = eval(patient_info[record_items.patient_record_items.index("last_visited_date")]).index(date)
        for record in self.changed_record.keys():
            if record in record_items.variable_records:
                old_record = eval(patient_info[record_items.patient_record_items.index(record)])
                old_record[date_index] = self.changed_record[record]  # old record updates with new data/record
                patient_info[record_items.patient_record_items.index(record)] = str(old_record)
            elif record == "date":
                patient_info[record_items.patient_record_items.index(record)] = self.changed_record[record]
                old_record = eval(patient_info[record_items.patient_record_items.index("last_visited_date")])
                old_record[date_index] = self.changed_record[record]  # old record updates with new data/record
                patient_info[record_items.patient_record_items.index("last_visited_date")] = str(old_record)
            else:
                patient_info[record_items.patient_record_items.index(record)] = self.changed_record[record]
        dataHandler.update_patient(self.patient_phone_number, patient_info)
        self.patient_phone_number = patient_info[record_items.patient_record_items.index("phone_number")]
        patient_manager.update_patient_list()
        screen_manager.show_dialog("Success", "Patient Record Updated Successfully")
        self.show_existing_record(tuple(patient_info), patient_info[record_items.patient_record_items.index("date")])

    def clear_textbox(self):
        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                self.findChild(pqw.QPlainTextEdit, item).setReadOnly(False)
                self.findChild(pqw.QPlainTextEdit, item).clear()
                self.findChild(pqw.QPlainTextEdit, item).setEnabled(True)
            else:
                if item == "necessary_images":
                    self.findChild(pqw.QPushButton, item).setText("Add Images")
                else:
                    self.findChild(pqw.QPushButton, item).setText("Add Videos")
                self.findChild(pqw.QPushButton, item).setEnabled(True)

        self.add_delete_record_button.setEnabled(True)
        self.edit_record_button.setEnabled(True)
        self.selected_image_directory.clear()
        self.selected_video_directory.clear()
        self.images_destination_directory = ""
        self.videos_destination_directory = ""

    def delete_record_confirmation(self, event):
        if event.text() == "&Yes":
            self.delete_record(self.opened_record_date)
            if eval(dataHandler.query_patient_info("last_visited_date", self.patient_phone_number)):
                self.clear_textbox()
                self.go_back_confirmation("actionGo_Back")
            else:
                dataHandler.delete_patient(self.patient_phone_number)
                screen_manager.show_screen("MainWindow")
                patient_manager.update_patient_list()
                screen_manager.widget.currentWidget().show_patient_list(patient_manager.patient_list)

    def delete_record(self, record_date):
        patient_info = list(dataHandler.fetch_patient(self.patient_phone_number))
        record_date_index = eval(patient_info[record_items.patient_record_items.index("last_visited_date")]).index(
            record_date)
        for item in record_items.variable_records:
            record = eval(patient_info[record_items.patient_record_items.index(item)])
            record.remove(record[record_date_index])
            patient_info[record_items.patient_record_items.index(item)] = str(record)
        dataHandler.update_patient(self.patient_phone_number, patient_info)
        screen_manager.show_dialog("Success", "Patient Record Deleted Successfully")

    def edit_patient_record(self):
        for item in record_items.patient_record_items:
            if item not in record_items.record_buttons:
                if item != "last_visited_date":
                    self.findChild(pqw.QPlainTextEdit, item).setEnabled(True)
                    self.findChild(pqw.QPlainTextEdit, item).setReadOnly(False)
                else:
                    self.findChild(pqw.QPlainTextEdit, item).setEnabled(False)
            else:
                self.findChild(pqw.QPushButton, item).setEnabled(True)

        self.edit_record_button.setEnabled(False)
        self.add_delete_record_button.setText("Update Record")

    def patient_exist_dialog(self, event):
        if event.text() == "&Yes":
            screen_manager.show_screen("PatientRecordUI",
                                       show_record_of=self.changed_record["phone_number"])
        else:
            self.changed_record.clear()

    def record_exist_dialog(self, event):
        if event.text() == "&Yes":
            self.patient_records.clear()
            self.show_existing_record(dataHandler.fetch_patient(self.patient_phone_number), self.changed_record["date"])

    def clear_changed_record(self):
        self.changed_record.clear()

    def select_media(self, media):
        patient_number = self.findChild(pqw.QPlainTextEdit, 'phone_number').toPlainText()
        record_date = self.findChild(pqw.QPlainTextEdit, 'date').toPlainText()
        root_dir = os.getcwd()
        os.makedirs(f"{root_dir}\\patient_data", exist_ok=True)
        if media == "images":

            # stores the directory of selected images
            # n.b -> it returns a tuple of (dir of selected files, extension of file selection e.g. ('directory',Custom)
            # this is why only the first index item is taken
            self.selected_image_directory = pqw.QFileDialog.getOpenFileNames(self,
                                                                             "Select Image(s)",
                                                                             root_dir,
                                                                             f"Custom Files {constants.image_extensions}")[
                0]

            # makes database directory for this particular patient on the particular record date
            self.images_destination_directory = f"{root_dir}\\patient_data\\{patient_number}\\{record_date}\\images"
            self.findChild(pqw.QPushButton, "necessary_images").setText("Images Selected")


        else:

            # stores the directory of selected videos
            self.selected_video_directory = pqw.QFileDialog.getOpenFileNames(self,
                                                                             "Select Image(s)",
                                                                             root_dir,
                                                                             f"Custom Files {constants.video_extensions}")[
                0]

            # makes database directory for this particular patient on the particular record date
            self.videos_destination_directory = f"{root_dir}\\patient_data\\{patient_number}\\{record_date}\\videos"
            self.findChild(pqw.QPushButton, "necessary_videos").setText("Videos Selected")

    def add_media(self):
        # make image, video directories
        os.makedirs(self.images_destination_directory, exist_ok=True)
        os.makedirs(self.videos_destination_directory, exist_ok=True)

        # stores the images into database folder (copy then delete : not cutting because of being aware)
        for image in self.selected_image_directory:
            shutil.copy2(image, self.images_destination_directory)

        # stores the videos into database folder (copy then delete : not cutting because of being aware)
        for video in self.selected_video_directory:
            shutil.copy2(video, self.videos_destination_directory)
