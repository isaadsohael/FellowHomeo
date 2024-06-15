import PyQt5.QtWidgets as pqw
import patient_info
import patient_record
import patient_manager

screens = ["MainWindow"]
widget = pqw.QStackedWidget()


def show_screen(screen):
    global screens
    global existing_patient_info
    if screen == "MainWindow":
        widget.setCurrentIndex(0)
        patient_manager.update_patient_list()
        widget.currentWidget().patient_list_widget.clear()
        for patient in patient_manager.patient_list:
            widget.currentWidget().patient_list_widget.addItem(
                f'{patient.get_info("name")} | {patient.get_info("phone_number")}')
    else:
        if screen == "PatientInfoUI":
            ui = patient_info.PatientInfoUI()
            widget.addWidget(ui)
            if screen not in screens:
                screens.append(screen)
            # widget.setCurrentIndex(screens.index(screen))
            widget.setCurrentWidget(ui)
        elif screen == "PatientRecordUI":
            ui = patient_record.PatientRecordUI()
            widget.addWidget(ui)
            if screen not in screens:
                screens.append(screen)
            widget.setCurrentIndex(screens.index(screen))
            widget.currentWidget().show_records()
