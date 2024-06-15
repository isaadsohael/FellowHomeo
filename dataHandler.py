import sqlite3
import patientClass
import record_items


def create_database():
    items = record_items.patient_record_items
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS patient_data({items[0]} text)""")
    db.commit()
    try:
        for v in range(1, len(items)):
            cursor.execute(f"""ALTER TABLE patient_data ADD {items[v]} text""")
            db.commit()
    except sqlite3.OperationalError:
        pass

    db.close()


def add_patient(patient_data: list):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""INSERT INTO patient_data VALUES (?,?,?,?,?,?,?,?)""", patient_data)
    db.commit()
    db.close()


def all_patients():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patient_data")
    data = cursor.fetchall()
    return data


def fetch_patient(phone_number):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patient_data WHERE phone_number = (?)", (phone_number,))
    data = cursor.fetchall()
    db.close()
    for query in data:
        return query


def query_patient_info(query_data, phone_number):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f"""SELECT {query_data} FROM patient_data WHERE phone_number = (?)""", (phone_number,))
    data = cursor.fetchall()
    db.close()
    return data[0][0]


def update_patient(phone_number, new_data: list):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    for item in record_items.patient_record_items:
        cursor.execute(f"""UPDATE patient_data SET {item} = (?) WHERE phone_number = (?)""",
                       (new_data[record_items.patient_record_items.index(item)], phone_number,))
        db.commit()
    db.close()


def delete_patient(phone_number):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM patient_data WHERE phone_number = (?)", (phone_number,))
    db.commit()
    db.close()
