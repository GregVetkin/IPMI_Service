from modules.config import IPMIServiceConfigReader
from modules.logger import Logger
from modules.ipmisensors import IpmitoolSensorsCollector, IPMISernsor, IPMIConnectionData, FAKEIpmitoolSensorsCollector
from modules.database.postgres import PostgresDatabase, IPMIPostgresDatabase



CONFIG_PATH = "./config.ini"

config = IPMIServiceConfigReader(CONFIG_PATH).get_service_config()


logger = Logger(config.logger)







db = IPMIPostgresDatabase(config.database)
devs = db.get_ipmi_devices_data()

for connection_data in devs:
    sensors = FAKEIpmitoolSensorsCollector(connection_data).collect()
    for sensor in sensors:
        print(sensor)