from dataclasses            import dataclass
from modules.database       import DatabaseIPMI
from modules.logger         import Logger
from modules.ipmi           import SensorsCollectorIPMI
from .cache                 import CacheIPMI
from modules.config.models  import ServiceConfig

@dataclass
class ServiceModules:
    module_db:             DatabaseIPMI
    module_logger:         Logger
    module_ipmi:           SensorsCollectorIPMI



@dataclass
class ServiceData:
    db:             DatabaseIPMI
    logger:         Logger
    ipmi:           SensorsCollectorIPMI
    config:         ServiceConfig
    cache:          CacheIPMI