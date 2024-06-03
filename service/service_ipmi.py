from modules.ipmisensors    import IPMISensor, IpmitoolSensorsCollector, IPMIConnectionData
from modules.database       import IPMIPostgresDatabase
from modules.logger         import Logger



class ServiceIPMI:
    def __init__(self, ipmi: IpmitoolSensorsCollector, database: IPMIPostgresDatabase, logger: Logger):
        self._ipmi  = ipmi
        self._db    = database
        self._log   = logger
        self._cache = None
        self._get_sensors_cache()


    def _get_sensors_cache(self):
        self._cache = {}
        BMCs = self._db.get_ipmi_connections_data()
        for bmc in BMCs:
            self._cache[bmc.host] = {}
            sensors = self._db.get_ipmi_sensors_data(bmc)
            for sensor in sensors:
                self._cache[bmc.host][sensor.name] = sensor
    
    def _sensor_cache_unchanged(self, bmc: IPMIConnectionData, sensor: IPMISensor):
        value = sensor.value
        sensor.value = None
        unchanged = sensor == self._cache[bmc.host][sensor.name]
        sensor.value = value
        return unchanged
    
    def _sensor_in_cache(self, bmc: IPMIConnectionData, sensor: IPMISensor):
        if bmc.host in self._cache:
            return sensor.name in self._cache[bmc.host]
        else:
            return False
        
    def sensor_data_check(self, bmc: IPMIConnectionData, sensor: IPMISensor):
        if not self._sensor_in_cache(bmc, sensor):
                self._db.insert_sensor_data(bmc, sensor)
        else:
            if not self._sensor_cache_unchanged(bmc, sensor):
                self._db.update_sensor_data(bmc, sensor)

    def record_bmc_sensors(self, bmc: IPMIConnectionData):
        ipmi = self._ipmi(bmc)
        sensors = ipmi.collect()

        for sensor in sensors:
            self.sensor_data_check(bmc, sensor)
            self._db.insert_sensor_value(bmc, sensor)
    

    def run(self):
        BMCs = self._db.get_ipmi_connections_data()
        for bmc in BMCs:
            self.record_bmc_sensors(bmc)
