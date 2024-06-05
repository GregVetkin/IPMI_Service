import  logging
import  logging.config
from    modules.config.models import LoggerConfig


LOG_LEVEL   = "DEBUG"
LOG_FORMAT  = '%(asctime)s---%(levelname)s---%(message)s'



class Logger:
    def __init__(self, config: LoggerConfig):
        self._config    = config
        self._logger    = logging.getLogger(__name__)
        self._configure_logger()

    def _configure_logger(self):
        self._set_log_level()
        self._set_file_handler()

    def _set_log_level(self):
        level = getattr(logging, LOG_LEVEL, logging.INFO)
        self._logger.setLevel(level)

    def _get_formatter(self):
        return logging.Formatter(LOG_FORMAT)
    
    def _set_file_handler(self):
        file_handler = logging.FileHandler(self._config.file)
        file_handler.setFormatter(self._get_formatter())
        self._logger.addHandler(file_handler)

    def debug(self, message: str):
        self._logger.debug(message)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def critical(self, message: str):
        self._logger.critical(message)
