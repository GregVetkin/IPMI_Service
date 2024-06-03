from modules.database   import DatabaseIPMI
from modules.ipmi       import Sensor, ConnectionData
from typing             import List


class CacheIPMI:
    def __init__(self, database: DatabaseIPMI) -> None:
        self._cache = {}
        self._db = database


    def _get_bmc_sensors(self, bmc: ConnectionData) -> List[Sensor]:
        return self._db.get_ipmi_sensors_data(bmc)


    def _get_all_bmc_connections(self) -> List[ConnectionData]:
        return self._db.get_ipmi_connections_data()

    def cache_all_bmc_sensors(self):
        self._cache = {}
        for bmc in self._get_all_bmc_connections():
            self._cache[bmc.address] = {}
            for sensor in self._get_bmc_sensors(bmc):
                self._cache[bmc.address][sensor.name] = sensor

    def sensor_unchanged(self, bmc: ConnectionData, sensor: Sensor) -> bool:
        value = sensor.value
        sensor.value = None
        unchanged = sensor == self._cache[bmc.address][sensor.name]
        sensor.value = value
        return unchanged
    
    def sensor_in_cache(self, bmc: ConnectionData, sensor: Sensor) -> bool:
        if bmc.address in self._cache:
            return sensor.name in self._cache[bmc.address]
        else:
            return False