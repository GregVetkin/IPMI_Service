from modules.ipmisensors import FAKEIpmitoolSensorsCollector
from modules.ipmisensors.models import IPMISernsor


sesors = FAKEIpmitoolSensorsCollector("s").collect()



class CorrectSensor:

    def _is_hex(self, value: str):
        return value.startswith("0x")
    
    def _is_NA(sef, value: str):
        return value == "na"
    

    def _fix_sensor_value(self, value: str):
        if self._is_NA(value):
            return None
        if self._is_hex(value):
            return int(value, base=16)
        return float(value)
    

    def _fix_sensor_status(self, value: str):
        if self._is_NA(value):
            return None
        return value
    
    def _fix_sensor_threshold(self, value: str):
        if self._is_NA(value):
            return None
        return float(value)
    

    def fix_sensor(self, sensor: IPMISernsor):
        sensor.value    = self._fix_sensor_value(sensor.value)

        sensor.status   = self._fix_sensor_status(sensor.status)
        sensor.lc       = self._fix_sensor_threshold(sensor.lc)
        sensor.lnc      = self._fix_sensor_threshold(sensor.lnc)
        sensor.lnr      = self._fix_sensor_threshold(sensor.lnr)
        sensor.uc       = self._fix_sensor_threshold(sensor.uc)
        sensor.unc      = self._fix_sensor_threshold(sensor.unc)
        sensor.unr      = self._fix_sensor_threshold(sensor.unr)
    


for sensor in sesors:
    CorrectSensor().fix_sensor(sensor)
    print(sensor)