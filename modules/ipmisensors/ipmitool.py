import subprocess
import re
from .models import IPMIConnectionData, IPMISernsor
from typing import List

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
                        

class IpmitoolSensorsCollector():
    def __init__(self, connection_data: IPMIConnectionData) -> None:
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
        r = ["sudo", "ipmitool", "-H", self._conn.host, "-U", self._conn.username, "-P", self._conn.password, "sensor", "list"]
        # l = ["sudo", "ipmitool", "sensor", "list"]
        # command = r if not local else l
        command = r
        result  = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    

    def collect(self) -> List[IPMISernsor]:
        sensors = []
        for sensor_data_str in self._ipmitool_data().splitlines():
            sensor_data_dic = self._parse_sensor_data(sensor_data_str)
            sensors.append(IPMISernsor(**sensor_data_dic))
        return sensors
    

