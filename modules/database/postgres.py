import psycopg2
from typing import List
from .database import Database
from modules.config.models import DatabaseConfig
from modules.ipmisensors import IPMIConnectionData



class PostgresDatabase(Database):
    def __init__(self, connection_config: DatabaseConfig):
        self._config        = connection_config
        self._connection    = None

    def _connect(self):
        self._connection = psycopg2.connect(
            dbname      = self._config.database,
            user        = self._config.username,
            password    = self._config.passowrd,
            host        = self._config.host,
            port        = self._config.port,
        )

    def _close(self):
        if self._connection:
            self._connection.close()

    def _execute_query(self, query, params=None):
        if not self._connection:
            self._connect()
        with self._connection.cursor() as cursor:
            cursor.execute(query, params)
            self._connection.commit()

    def _fetch_results(self, query, params=None):
        if not self._connection:
            self._connect()
        with self._connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
        return results



class IPMIPostgresDatabase(PostgresDatabase):
    def __init__(self, connection_config: DatabaseConfig):
        super().__init__(connection_config)
    
    def get_ipmi_devices_data(self) -> List[IPMIConnectionData]:
        ipmi_devices    = []
        query           = """SELECT * FROM ipmi_dev;"""
        result          = self._fetch_results(query)
        for _ in result:
            ipmi_devices.append(
                IPMIConnectionData(
                    host     = _[1],
                    username = _[2],
                    password = _[3],
                )
            )
        return ipmi_devices
    