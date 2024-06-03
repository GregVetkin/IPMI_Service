from modules.ipmisensors    import Sensor, IpmitoolSensorsCollector, ConnectionData
from modules.database       import DatabaseIPMI
from modules.logger         import Logger
from typing                 import List



class ServiceIPMI:
    def __init__(self, ipmi: IpmitoolSensorsCollector, database: DatabaseIPMI, logger: Logger):
        self._ipmi  = ipmi
        self._db    = database
        self._log   = logger
        self._cache = None
        self._get_sensors_cache()


    def _get_sensors_cache(self):
        self._cache = {}
        for bmc in self._db.get_ipmi_connections_data():
            self._cache[bmc.host] = {}
            sensors = self._db.get_ipmi_sensors_data(bmc)
            for sensor in sensors:
                self._cache[bmc.host][sensor.name] = sensor
    
    def _sensor_cache_unchanged(self, bmc: ConnectionData, sensor: Sensor):
        value = sensor.value
        sensor.value = None
        unchanged = sensor == self._cache[bmc.host][sensor.name]
        sensor.value = value
        return unchanged
    
    def _sensor_in_cache(self, bmc: ConnectionData, sensor: Sensor):
        if bmc.host in self._cache:
            return sensor.name in self._cache[bmc.host]
        else:
            return False
        
    def _sensor_data_check(self, bmc: ConnectionData, sensor: Sensor):
        if not self._sensor_in_cache(bmc, sensor):
                self._db.insert_sensor_data(bmc, sensor)
        else:
            if not self._sensor_cache_unchanged(bmc, sensor):
                self._db.update_sensor_data(bmc, sensor)


    def record_bmc_sensors(self, bmc: ConnectionData):
        for sensor in self._ipmi(bmc).collect():
            self._sensor_data_check(bmc, sensor)
            self._db.insert_sensor_value(bmc, sensor)
    
    def run(self):
        for bmc in self._db.get_ipmi_connections_data():
            self.record_bmc_sensors(bmc)
