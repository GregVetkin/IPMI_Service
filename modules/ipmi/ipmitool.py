import subprocess
import re
from .models    import ConnectionData, Sensor
from .base      import SensorsCollectorIPMI
from typing     import List


IPMITOOL_PATTERN =  r"^"                                               + \
                    r"(?P<name>[\w\s\.]+)\s*\|\s*"                     + \
                    r"(?P<value>[\d\.]+|na|0x[0-9a-fA-F]+)\s*\|\s*"    + \
                    r"(?P<unit>[\w\s]+|na)\s*\|\s*"                    + \
                    r"(?P<status>\w+|na|0x[0-9a-fA-F]+)\s*\|\s*"       + \
                    r"(?P<lnr>[\d\.]+|na)\s*\|\s*"                     + \
                    r"(?P<lc>[\d\.]+|na)\s*\|\s*"                      + \
                    r"(?P<lnc>[\d\.]+|na)\s*\|\s*"                     + \
                    r"(?P<unc>[\d\.]+|na)\s*\|\s*"                     + \
                    r"(?P<uc>[\d\.]+|na)\s*\|\s*"                      + \
                    r"(?P<unr>[\d\.]+|na)\s*"                          + \
                    r"$"
                        



class IpmitoolSensorsCollector(SensorsCollectorIPMI):
    def __init__(self, connection_data: ConnectionData) -> None:
        self._conn = connection_data


    def _parse_sensor_data(self, data: str) -> dict:
        sensor_data = {}
        pattern     = re.compile(IPMITOOL_PATTERN)
        match       = pattern.match(data)
        if match:
            sensor_data = match.groupdict()
            self._space_cleaner(sensor_data)
        return sensor_data


    def _space_cleaner(self, sensor_data: dict):
        for _ in sensor_data:
            sensor_data[_] = sensor_data[_].strip()


    def _ipmitool_data(self) -> str:
        r = ["sudo", "ipmitool", "-H", self._conn.address, "-U", self._conn.username, "-P", self._conn.password, "sensor", "list"]
        # l = ["sudo", "ipmitool", "sensor", "list"]
        # command = r if not local else l
        command = r
        result  = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    

    def collect(self) -> List[Sensor]:
        sensors = []
        for sensor_data_str in self._ipmitool_data().splitlines():
            sensor_data_dic = self._parse_sensor_data(sensor_data_str)
            sensor = Sensor(**sensor_data_dic)
            CorrectSensor().fix_sensor(sensor)
            sensors.append(sensor)
        return sensors
    



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
    

    def fix_sensor(self, sensor: Sensor):
        sensor.value    = self._fix_sensor_value(sensor.value)

        sensor.status   = self._fix_sensor_status(sensor.status)
        sensor.lc       = self._fix_sensor_threshold(sensor.lc)
        sensor.lnc      = self._fix_sensor_threshold(sensor.lnc)
        sensor.lnr      = self._fix_sensor_threshold(sensor.lnr)
        sensor.uc       = self._fix_sensor_threshold(sensor.uc)
        sensor.unc      = self._fix_sensor_threshold(sensor.unc)
        sensor.unr      = self._fix_sensor_threshold(sensor.unr)
    

