from modules.database   import DatabaseIPMI
from modules.ipmi       import Sensor, ConnectionData
from modules.logger     import Logger
from typing             import List

import sys


class CacheIPMI:
    def __init__(self, database: DatabaseIPMI, logger: Logger) -> None:
        self._cache = {}
        self._db    = database
        self._log   = logger


    def _get_bmc_sensors(self, bmc: ConnectionData) -> List[Sensor]:
        try:
            self._log.debug(f"Получение данных сенсоров устрйоства с адрессом {bmc.address} для добавления в кэш")
            result = self._db.get_ipmi_sensors_data(bmc)
        except Exception as e:
            self._log.critical(f"Не удалось получить данные сенсоров для устройства {bmc.address} из базы данных. Вызвано исключение: {e}")
            sys.exit(1)
        return result


    def _get_all_bmc_connections(self) -> List[ConnectionData]:
        try:
            self._log.debug(f"Получение данных всех bmc из базы данных")
            result = self._db.get_ipmi_connections_data()
        except Exception as e:
            self._log.critical(f"Не удалось получить данные bmc из базы данных. Вызвано исключение: {e}")
            sys.exit(1)
        return result



    def cache_all_bmc_sensors(self):
        self._cache = {}
        for bmc in self._get_all_bmc_connections():
            if not bmc.address in self._cache:
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
        return False