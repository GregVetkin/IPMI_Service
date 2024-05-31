from modules.config import IPMIServiceConfigReader
from modules.logger import Logger
from modules.ipmisensors import IpmitoolSensorsCollector, IPMISernsor, IPMIConnectionData, FAKEIpmitoolSensorsCollector




CONFIG_PATH = "./config.ini"

config = IPMIServiceConfigReader(CONFIG_PATH).get_service_config()


logger = Logger(config.logger)
logger.info(f"test {config.database.database}")







connection_data = IPMIConnectionData(
    host        = "192.168.0.240",
    username    = "admin",
    password    = "admin",
)

sensors = FAKEIpmitoolSensorsCollector(connection_data).collect()


for _ in sensors:
    print(_)
    