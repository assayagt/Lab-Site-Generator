from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def some_operation(self):
        pass