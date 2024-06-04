from modules.ipmi           import Sensor, ConnectionData
from typing                 import List
from .models                import ServiceData
from time                   import sleep
import concurrent.futures







class ServiceIPMI:
    def __init__(self, service_data: ServiceData):
        self._config    = service_data.config
        self._ipmi      = service_data.ipmi
        self._db        = service_data.db
        self._log       = service_data.logger
        self._cache     = service_data.cache
        self._cache.cache_all_bmc_sensors()
        self._interval  = self._config.worker.interval


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
        while True:
            print("start")
            BMCs = self._db.get_ipmi_connections_data()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self._record_bmc_sensors, BMCs)
            print("end")
            sleep(self._interval)
