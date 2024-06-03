from modules.ipmi           import Sensor, ConnectionData, SensorsCollectorIPMI
from modules.database       import DatabaseIPMI
from modules.logger         import Logger
from typing                 import List
from .cache                 import CacheIPMI
import concurrent.futures




class ServiceIPMI:
    def __init__(self, ipmi: SensorsCollectorIPMI, database: DatabaseIPMI, logger: Logger):
        self._ipmi  = ipmi
        self._db    = database
        self._log   = logger
        self._cache = CacheIPMI(self._db)
        self._cache.cache_all_bmc_sensors()


    def _sensor_data_check(self, bmc: ConnectionData, sensor: Sensor):
        if not self._cache.sensor_in_cache(bmc, sensor):
            self._db.insert_sensor_data(bmc, sensor)
        elif not self._cache.sensor_unchanged(bmc, sensor):
            self._db.update_sensor_data(bmc, sensor)


    def _record_bmc_sensors(self, bmc: ConnectionData):
        for sensor in self._ipmi(bmc).collect():
            self._sensor_data_check(bmc, sensor)
            self._db.insert_sensor_value(bmc, sensor)
    

    def run(self):
        BMCs = self._db.get_ipmi_connections_data()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self._record_bmc_sensors, BMCs)
        
