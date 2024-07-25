import PyQt5.QtWidgets as pqw
from screens import main_screen, patient_info_screen, patient_record_screen
import sys

screens = []
widget = pqw.QStackedWidget()
widget.resize(550, 400)
widget.setWindowTitle("FellowHomeo")


def show_screen(screen, show_record_of=""):
    global screens
    if screen == "MainWindow":
        ui = main_screen.UI()
        widget.addWidget(ui)
        if screen not in screens:
            screens.append(screen)
        widget.setCurrentWidget(ui)

        # destroying other screens except current screen
        for v in range(len(widget)):
            if widget.widget(v) != "MainWindow":
                destroy_screen(widget.widget(v))
        screens.clear()
        screens.append("MainWindow")

    else:
        if screen == "PatientInfoUI":
            ui = patient_info_screen.PatientInfoUI()
            widget.addWidget(ui)
            if screen not in screens:
                screens.append(screen)
            # widget.setCurrentIndex(screens.index(screen))
            widget.setCurrentWidget(ui)
            widget.currentWidget().show_info_of(show_record_of)

            # destroying other screens except current screen
            for v in range(len(widget)):
                if widget.widget(v) != "PatientInfoUI":
                    destroy_screen(widget.widget(v))
            screens.clear()
            screens.append("MainWindow")

        elif screen == "PatientRecordUI":
            ui = patient_record_screen.PatientRecordUI()
            widget.addWidget(ui)
            if screen not in screens:
                screens.append(screen)
            widget.setCurrentWidget(ui)
            widget.currentWidget().show_records(show_record_of)

            # destroying other screens except current screen
            for v in range(len(widget)):
                if widget.widget(v) != "PatientRecordUI":
                    destroy_screen(widget.widget(v))
            screens.clear()
            screens.append("MainWindow")


def show_dialog(title, text, detailed_text="", do_what=""):
    dialog = pqw.QMessageBox()
    if do_what == "delete_patient":
        dialog.setIcon(pqw.QMessageBox.Question)
        dialog.setStandardButtons(pqw.QMessageBox.Yes | pqw.QMessageBox.Abort)
        dialog.buttonClicked.connect(widget.currentWidget().delete_patient)
    elif do_what == "delete_record":
        dialog.setIcon(pqw.QMessageBox.Question)
        dialog.setStandardButtons(pqw.QMessageBox.Yes | pqw.QMessageBox.Abort)
        dialog.buttonClicked.connect(widget.currentWidget().delete_record_confirmation)
    elif do_what == "quit":
        dialog.setIcon(pqw.QMessageBox.Question)
        dialog.setStandardButtons(pqw.QMessageBox.Yes | pqw.QMessageBox.No)
        dialog.buttonClicked.connect(quit_app)
    elif do_what == "go_back_warning":
        dialog.setIcon(pqw.QMessageBox.Warning)
        dialog.setStandardButtons(pqw.QMessageBox.Yes | pqw.QMessageBox.Abort)
        dialog.buttonClicked.connect(widget.currentWidget().go_back)
    elif do_what == "update":
        dialog.setIcon(pqw.QMessageBox.Question)
        dialog.setStandardButtons(pqw.QMessageBox.Yes | pqw.QMessageBox.Abort)
        dialog.buttonClicked.connect(widget.currentWidget().update_patient_record)
    elif do_what == "patient_exists":
        dialog.setIcon(pqw.QMessageBox.Warning)
        dialog.setStandardButtons(pqw.QMessageBox.Yes | pqw.QMessageBox.Abort)
        dialog.buttonClicked.connect(widget.currentWidget().patient_exist_dialog)
        dialog.destroyed.connect(widget.currentWidget().clear_changed_record)
    elif do_what == "record_exists":
        dialog.setIcon(pqw.QMessageBox.Warning)
        dialog.setStandardButtons(pqw.QMessageBox.Yes | pqw.QMessageBox.Abort)
        dialog.buttonClicked.connect(widget.currentWidget().record_exist_dialog)
        dialog.destroyed.connect(widget.currentWidget().clear_changed_record)
    else:
        dialog.setIcon(pqw.QMessageBox.Information)
    dialog.setWindowTitle(title)
    dialog.setText(text)
    dialog.setDetailedText(detailed_text)
    dialog.exec_()


def quit_app(event):
    if event.text() == "&Yes":
        sys.exit()


def destroy_screen(screen_name):
    widget.removeWidget(screen_name)
