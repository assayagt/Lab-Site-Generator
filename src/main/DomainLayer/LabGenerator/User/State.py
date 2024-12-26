from abc import ABC, abstractmethod

class State(ABC):

    @abstractmethod
    def get_member_id(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def exit_Generator_system(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def is_member(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_email(self):
        pass
