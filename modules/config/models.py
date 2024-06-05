from dataclasses import dataclass


@dataclass
class WorkerConfig:
    interval:   float


@dataclass
class DatabaseConfig:
    database:   str = "postgres"
    username:   str = "postgres"
    passowrd:   str = "postgres"
    host:       str = "localhost"
    port:       int = 5432


@dataclass
class LoggerConfig:
    file:       str = "./logs.log"
    level:      str = "DEBUG"
    max_size:   int = 100 * 1024 * 1024     # 100mb


@dataclass
class ServiceConfig:
    database:   DatabaseConfig
    worker:     WorkerConfig
    logger:     LoggerConfig
