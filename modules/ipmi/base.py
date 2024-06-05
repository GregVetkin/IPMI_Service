from abc        import ABC, abstractmethod
from typing     import List
from .models    import Sensor


class SensorsCollectorIPMI(ABC):
    @abstractmethod
    def collect(self) -> List[Sensor]:
        pass