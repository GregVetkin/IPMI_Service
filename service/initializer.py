from .service_ipmi          import ServiceIPMI
from .models                import ServiceData, ServiceModules
from .cache                 import CacheIPMI
from modules.config         import ServiceConfigReader






class ServiceCreator:
    def __init__(self, config_path, modules: ServiceModules) -> None:
        self._modules       = modules
        self._config        = self._init_config(config_path)
        self._ipmi          = self._init_ipmi()
        self._db            = self._init_database()
        self._log           = self._init_logger()
        self._cache         = self._init_cache()


    def _init_config(self, config_path):
        return ServiceConfigReader(config_path).get_service_config()

    def _init_database(self):
        return self._modules.module_db(self._config.database)

    def _init_logger(self):
        return self._modules.module_logger(self._config.logger)
    
    def _init_ipmi(self):
        return self._modules.module_ipmi
    
    def _init_cache(self):
        if self._db is None:
            self._init_database()
        return CacheIPMI(self._db, self._log)

    def _get_ServiceData(self):
        return ServiceData(
            ipmi    = self._ipmi,
            db      = self._db,
            logger  = self._log,
            config  = self._config,
            cache   = self._cache
        )

    def create_service(self) -> ServiceIPMI:
        return ServiceIPMI(
            self._get_ServiceData()
        )