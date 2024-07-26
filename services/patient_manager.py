import os
import shutil
import sqlite3
from services import patientClass, dataHandler, resource_path, constants, screen_manager

try:
    patient_list = [patientClass.Patient(patient) for patient in dataHandler.all_patients()]
except sqlite3.OperationalError:
    patient_list = []


def update_patient_list():
    global patient_list
    patient_list.clear()
    patient_list = [patientClass.Patient(patient) for patient in dataHandler.all_patients()]


def patient_exists(phone_number):
    if phone_number in [patient.get_info("phone_number") for patient in patient_list]:
        return True
    else:
        return False


def remove_media(media):
    try:
        os.remove(media)
    except FileNotFoundError:
        pass


def remove_patient_data(phone_number):
    try:
        shutil.rmtree(resource_path.resource_path(f"{constants.media_directory_name}\\{phone_number}"))
        dataHandler.delete_patient(phone_number)
    except FileNotFoundError:
        pass
    except PermissionError:
        screen_manager.show_dialog("Warning", "File In Use")
