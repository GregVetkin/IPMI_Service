from modules.logger             import Logger
from modules.ipmi               import IpmitoolSensorsCollector, FAKESensorsCollector
from modules.database           import PostgresDatabaseIPMI


from service.models             import ServiceModules
from service.initializer        import ServiceCreator


if __name__ == "__main__":
    CONFIG_PATH = "./config.ini"
    modules = ServiceModules(
        module_db       = PostgresDatabaseIPMI,
        module_ipmi     = FAKESensorsCollector,
        module_logger   = Logger,
    )
    service = ServiceCreator(CONFIG_PATH, modules).create_service()
    service.run()