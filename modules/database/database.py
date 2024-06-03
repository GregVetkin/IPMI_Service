from abc                    import ABC, abstractmethod
from typing                 import List
from modules.ipmi           import ConnectionData, Sensor



class Database(ABC):
    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _close(self):
        pass

    @abstractmethod
    def _execute_query(self, query, params=None):
        pass

    @abstractmethod
    def _fetch_results(self, query, params=None):
        pass



class DatabaseIPMI(ABC):
    @abstractmethod
    def get_ipmi_connections_data(self) -> List[ConnectionData]:
        pass

    @abstractmethod
    def get_ipmi_sensors_data(self, bmc: ConnectionData) -> List[Sensor]:
        pass

    @abstractmethod
    def update_sensor_data(self, bmc: ConnectionData, sensor: Sensor):
        pass

    @abstractmethod
    def insert_sensor_data(self, bmc: ConnectionData, sensor: Sensor):
        pass

    @abstractmethod
    def insert_sensor_value(self, bmc: ConnectionData, sensor: Sensor):
        pass