class ContactInfo:
    def __init__(self, lab_address, lab_mail, lab_phone_num):
        self.lab_address = lab_address
        self.lab_mail = lab_mail
        self.lab_phone_num = lab_phone_num

    def set_lab_address(self, lab_address):
        self.lab_address = lab_address

    def set_lab_mail(self, lab_mail):
        self.lab_mail = lab_mail

    def set_phone_num(self, lab_phone_num):
        self.lab_phone_num = lab_phone_num

    def get_lab_address(self):
        return self.lab_address
    
    def get_lab_mail(self):
        return self.lab_mail
    
    def get_lab_phone_num(self):
        return self.lab_phone_num
    
    def to_dict(self):
        return {
            "address": self.lab_address,
            "email": self.lab_mail,
            "phone_num": self.lab_phone_num
        }