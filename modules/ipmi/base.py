from abc import ABC, abstractmethod



class SensorsCollectorIPMI(ABC):
    @abstractmethod
    def collect(self):
        pass