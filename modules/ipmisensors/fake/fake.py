from ..models    import IPMIConnectionData
from ..ipmitool  import IpmitoolSensorsCollector


class FAKEIpmitoolSensorsCollector(IpmitoolSensorsCollector):
    def __init__(self, connection_data: IPMIConnectionData):
        super().__init__(connection_data)
    
    def _ipmitool_data(self) -> str:
        data = ""
        with open("./modules/ipmisensors/fake/ipmitool_output.txt", "r") as file:
            data += file.read()
        return data