import psycopg2
from .database import Database
from modules.config.models import DatabaseConfig




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
        with self._connection.cursor() as cursor:
            cursor.execute(query, params)
            self._connection.commit()

    def _fetch_results(self, query, params=None):
        with self._connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
        return results

