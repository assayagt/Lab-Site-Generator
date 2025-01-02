class Response:
    def __init__(self, data=None, message=""):
        self.message = message
        self.data = data
        self.success = data is not None

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def is_success(self):
        return self.success

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
