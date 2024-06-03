import psycopg2

from typing                     import List
from .database                  import Database, DatabaseIPMI

from modules.config.models      import DatabaseConfig
from modules.ipmi               import ConnectionData, Sensor




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



class PostgresDatabaseIPMI(PostgresDatabase, DatabaseIPMI):
    def __init__(self, connection_config: DatabaseConfig):
        super().__init__(connection_config)
    
    def get_ipmi_connections_data(self) -> List[ConnectionData]:
        ipmi_devices    = []
        query           = """SELECT address, username, password FROM IPMI.BMC;"""
        result          = self._fetch_results(query)
        for _ in result:
            ipmi_devices.append(
                ConnectionData(
                    address  = _[0],
                    username = _[1],
                    password = _[2],
                )
            )
        return ipmi_devices
    

    def get_ipmi_sensors_data(self, bmc: ConnectionData) -> List[Sensor]:
        sensors = []
        query   = """
            SELECT
                s.name,
                s.unit,
                s.status,
                s.lnr,
                s.lc,
                s.lnc,
                s.unc,
                s.uc,
                s.unr
            FROM 
                IPMI.SENSORS as s
            JOIN 
                IPMI.BMC as b ON s.bmc_id = b.id
            WHERE b.address = %s;
        """
        result          = self._fetch_results(query, [bmc.address,])

        for _ in result:
            sensors.append(
                Sensor(
                    name    = _[0],
                    unit    = _[1],
                    status  = _[2],
                    lnr     = _[3],
                    lc      = _[4],
                    lnc     = _[5],
                    unc     = _[6],
                    uc      = _[7],
                    unr     = _[8],
                )
            )
        return sensors
        

    def update_sensor_data(self, bmc: ConnectionData, sensor: Sensor):
        query = """
            UPDATE 
                IPMI.SENSORS
            SET
                unit      = %s,
                status    = %s,
                lnr       = %s,
                lc        = %s,
                lnc       = %s,
                unc       = %s,
                uc        = %s,
                unr       = %s
            WHERE
                name      = %s
            AND 
                bmc_id    = (SELECT id FROM IPMI.BMC WHERE address = %s)
            ;
        """

        self._execute_query(query, params=[
            sensor.unit,
            sensor.status,
            sensor.lnr,
            sensor.lc,
            sensor.lnc,
            sensor.unc,
            sensor.uc,
            sensor.unr,
            sensor.name,
            bmc.address,
        ])


    def insert_sensor_data(self, bmc: ConnectionData, sensor: Sensor):
        query = """
        INSERT INTO
            IPMI.SENSORS
            (
                bmc_id, 
                name, 
                unit, 
                status, 
                lnr, 
                lc, 
                lnc, 
                unc, 
                uc, 
                unr
            )
        VALUES
            (
                (SELECT id FROM IPMI.BMC WHERE address = %s),
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s
            )
        ;
        """

        self._execute_query(query, params=[
            bmc.address,
            sensor.name,
            sensor.unit,
            sensor.status,
            sensor.lnr,
            sensor.lc,
            sensor.lnc,
            sensor.unc,
            sensor.uc,
            sensor.unr,
        ])


    def insert_sensor_value(self, bmc: ConnectionData, sensor: Sensor):
        query = """
        INSERT INTO 
            IPMI.SENSORS_VALUE (sensor_id, value)

        SELECT s.id, %s
        FROM 
            IPMI.SENSORS as s
        JOIN 
            IPMI.BMC as b ON s.bmc_id = b.id
        WHERE 
            s.name = %s 
        AND 
            b.address = %s
        ;
        """
        self._execute_query(query, params=[
            sensor.value,
            sensor.name,
            bmc.address,
        ])


    