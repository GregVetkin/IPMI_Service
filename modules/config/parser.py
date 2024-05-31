import configparser
from .models import IPMIServiceConfig, DatabaseConfig, LoggerConfig, WorkerConfig


SECTION_DATABASE            = "DATABASE"
PARAMETER_DATABASE_NAME     = "db_name"
PARAMETER_DATABASE_USER     = "db_user"
PARAMETER_DATABASE_PASS     = "db_pass"
PARAMETER_DATABASE_HOST     = "db_host"
PARAMETER_DATABASE_PORT     = "db_port"

SECTION_WORKER              = "WORKER"
PARAMETER_WORKER_INTERVAL   = "interval"

SECTION_LOGS                = "LOGS"
PARAMETER_LOGS_LOGFILE      = "log_file"


class IPMIServiceConfigReader:
    def __init__(self, config_file):
        self._config = self._parse_config_file(config_file)

    def _parse_config_file(self, config_file) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    
    def _get_worker_configuration(self) -> WorkerConfig:
        return WorkerConfig(
            interval = self._config.getfloat(SECTION_WORKER, PARAMETER_WORKER_INTERVAL)
        )

    def _get_database_configuration(self) -> DatabaseConfig:
        return DatabaseConfig(
            database = self._config.get(SECTION_DATABASE, PARAMETER_DATABASE_NAME),
            username = self._config.get(SECTION_DATABASE, PARAMETER_DATABASE_USER),
            passowrd = self._config.get(SECTION_DATABASE, PARAMETER_DATABASE_PASS),
            host     = self._config.get(SECTION_DATABASE, PARAMETER_DATABASE_HOST),
            port     = self._config.getint(SECTION_DATABASE, PARAMETER_DATABASE_PORT),
        )

    def _get_logger_configuration(self) -> LoggerConfig:
        return LoggerConfig(
            file = self._config.get(SECTION_LOGS, PARAMETER_LOGS_LOGFILE),
        )
    
    def get_service_config(self) -> IPMIServiceConfig:
        return IPMIServiceConfig(
            database    = self._get_database_configuration(),
            worker      = self._get_worker_configuration(),
            logger      = self._get_logger_configuration(),
        )

