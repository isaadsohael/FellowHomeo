import record_items


class Patient:
    def __init__(self, patient_info: tuple):
        self.patient = {}
        i = 0
        for items in record_items.patient_record_items:
            self.patient[items] = patient_info[i]
            i += 1

    def get_info(self, info):
        return self.patient[info]
