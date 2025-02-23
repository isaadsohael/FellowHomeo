import PyQt5.QtWidgets as pqw
from PyQt5 import uic
from services import patient_manager, screen_manager, constants
from services import resource_path


class UI(pqw.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        # main screen ui declaration
        self.ui = resource_path.resource_path(constants.main_screen_dir)
        # load ui
        uic.loadUi(self.ui, self)

        self.isSelected = False
        self.selectedWidgetText = ""

        # display patient list on main screen as list of widget
        self.show_patient_list(patient_manager.patient_list)

        self.patient_list_widget = self.findChild(pqw.QListWidget, constants.patient_list_widget)
        self.patient_list_widget.itemDoubleClicked.connect(self.go_to_patient_record_screen)
        self.patient_list_widget.itemClicked.connect(self.unselect_item)

        self.view_patient_button = self.findChild(pqw.QPushButton, constants.view_patient_button)
        self.view_patient_button.clicked.connect(self.go_to_patient_record_screen)

        self.create_new_patient = self.findChild(pqw.QAction, constants.actionCreate_New_Patient)
        self.create_new_patient.triggered.connect(self.new_patient_screen)

        self.delete_patient_action = self.findChild(pqw.QAction, constants.actionDelete_Patient)
        self.delete_patient_action.triggered.connect(
            lambda x: screen_manager.show_dialog("Warning", "Are you sure you want to delete the person?",
                                                 detailed_text=f"All Records of this patient will be deleted:\n{self.patient_list_widget.currentItem().text()}" if self.patient_list_widget.currentItem().isSelected() else "",
                                                 do_what="delete_patient") if self.isSelected else screen_manager.show_dialog(
                "Warning", "No Patient Selected"))

        self.search_bar = self.findChild(pqw.QLineEdit, constants.search_textbox)
        self.search_bar.returnPressed.connect(self.search_patients)
        self.search_bar.textChanged.connect(self.search_patients)

        self.clear_search_button = self.findChild(pqw.QPushButton, constants.clear_search_button)
        self.clear_search_button.clicked.connect(lambda x: self.search_bar.setText(""))

        self.findChild(pqw.QAction, constants.actionQuit).triggered.connect(
            lambda x: screen_manager.show_dialog("Confirm QUIT",
                                                 "Are you sure you want to close the app?",
                                                 detailed_text="",
                                                 do_what="quit"))

    def unselect_item(self):
        if self.isSelected:
            if self.patient_list_widget.currentItem().text() == self.selectedWidgetText:
                self.patient_list_widget.currentItem().setSelected(False)
                self.isSelected = False
            else:
                self.selectedWidgetText = self.patient_list_widget.currentItem().text()
        else:
            self.selectedWidgetText = self.patient_list_widget.currentItem().text()
            self.isSelected = True

    def go_to_patient_record_screen(self):
        if self.isSelected:
            screen_manager.show_screen("PatientRecordUI",
                                       show_record_of=self.patient_list_widget.currentItem().text().split("|")[
                                           -1].rstrip().lstrip())
        else:
            screen_manager.show_dialog("Information", "Select Patient To View!")

    def show_patient_list(self, patient_list):
        self.patient_list_widget.clear()
        for patient in patient_list:
            self.patient_list_widget.addItem(f'{patient.get_info("name")} | {patient.get_info("phone_number")}')

    def new_patient_screen(self):
        screen_manager.show_screen("PatientInfoUI")
        screen_manager.widget.currentWidget().show_new_patient_screen()

    def search_patients(self):
        if self.search_bar.text() != "":
            matched_patients = [patients for patients in patient_manager.patient_list if
                                self.search_bar.text().lower() == patients.get_info(
                                    "name").lower()[:len(
                                    self.search_bar.text())] or self.search_bar.text() in patients.get_info(
                                    "phone_number")[:len(self.search_bar.text())]]
            self.patient_list_widget.clear()
            self.show_patient_list(matched_patients)
        else:
            self.patient_list_widget.clear()
            self.show_patient_list(patient_manager.patient_list)

    def delete_patient(self, event):
        if event.text() == "&Yes":
            if self.patient_list_widget.currentItem().isSelected():
                patient_phone_number = patient_manager.patient_list[self.patient_list_widget.currentRow()].get_info(
                    "phone_number")
                patient_manager.remove_patient_data(patient_phone_number)
                patient_manager.update_patient_list()
                self.patient_list_widget.clear()
                self.show_patient_list(patient_manager.patient_list)
            else:
                screen_manager.show_dialog("Warning", "No Patient Selected")
