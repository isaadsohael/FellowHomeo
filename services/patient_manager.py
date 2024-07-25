import sqlite3
from services import patientClass, dataHandler

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
