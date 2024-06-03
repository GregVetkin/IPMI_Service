from modules.config             import IPMIServiceConfigReader
from modules.logger             import Logger
from modules.ipmisensors        import IpmitoolSensorsCollector, FAKEIpmitoolSensorsCollector
from modules.database           import IPMIPostgresDatabase
from service                    import ServiceIPMI
from time                       import sleep







if __name__ == "__main__":
    CONFIG_PATH = "./config.ini"

    config      = IPMIServiceConfigReader(CONFIG_PATH).get_service_config()
    interval    = config.worker.interval

    ipmi        = FAKEIpmitoolSensorsCollector
    logger      = Logger(config.logger)
    db          = IPMIPostgresDatabase(config.database)

    service     = ServiceIPMI(ipmi, db, logger)

    while True:
        service.run()
        sleep(interval)
