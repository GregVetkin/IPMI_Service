from ..models    import ConnectionData
from ..ipmitool  import IpmitoolSensorsCollector


class FAKESensorsCollector(IpmitoolSensorsCollector):
    def __init__(self, connection_data: ConnectionData):
        super().__init__(connection_data)
    
    def _ipmitool_data(self) -> str:
        data = ""
        with open("./modules/ipmi/fake/ipmitool_output.txt", "r") as file:
            data += file.read()
        return data