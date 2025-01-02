from abc import ABC, abstractmethod

class State(ABC):

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def is_member(self):
        pass

    @abstractmethod
    def get_email(self):
        pass
