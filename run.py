from modules.config             import ServiceConfigReader
from modules.logger             import Logger
from modules.ipmisensors        import IpmitoolSensorsCollector, FAKESensorsCollector
from modules.database           import PostgresDatabaseIPMI
from service                    import ServiceIPMI
from time                       import sleep







if __name__ == "__main__":
    CONFIG_PATH = "./config.ini"

    config      = ServiceConfigReader(CONFIG_PATH).get_service_config()
    interval    = config.worker.interval

    ipmi        = IpmitoolSensorsCollector
    logger      = Logger(config.logger)
    db          = PostgresDatabaseIPMI(config.database)

    service     = ServiceIPMI(ipmi, db, logger)

    while True:
        try:
            logger.info("Начало сбора")
            service.run()
        except Exception as e:
            logger.error(str(e))
        else:
            logger.info("Сбор сенсоров успешно закончен")
        sleep(interval)
