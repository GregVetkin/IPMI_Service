from modules.ipmi           import Sensor, ConnectionData
from typing                 import List
from .models                import ServiceData
from time                   import sleep
import concurrent.futures

import sys





class ServiceIPMI:
    def __init__(self, service_data: ServiceData):
        self._config    = service_data.config
        self._ipmi      = service_data.ipmi
        self._db        = service_data.db
        self._log       = service_data.logger
        self._cache     = service_data.cache

        self._check_database()
        self._cache.cache_all_bmc_sensors()
        self._interval  = self._config.worker.interval # or self._db.get_polling_interval()
        self._control   = {}

    def _check_database(self):
        try:
            self._log.info("Проверка подключения к базе данных")
            self._db._connect()
        except Exception as e:
            self._log.critical(f"Нет подключения к базе данных. Вызвано исключение: {e}")
        else:
            self._log.info("Соединение с базой данных установлено")




    def _db_insert_sensor_data(self, bmc: ConnectionData, sensor: Sensor):
        try:
            self._log.info(f"Добавление нового сенсора [{bmc.address}][{sensor.name}] в базу данных.")
            self._db.insert_sensor_data(bmc, sensor)
        except Exception as e:
            self._log.warning(f"Не удалось добавить новый сенсор [{bmc.address}][{sensor.name}] в базу данных. Вызвано исключение: {e}")
        else:
            self._log.info(f"Сенсор [{bmc.address}][{sensor.name}] успешно добавлен.")

    def _db_update_sensor_data(self, bmc: ConnectionData, sensor: Sensor):
        try:
            self._log.info(f"Обновление данных для сенсора [{bmc.address}][{sensor.name}].")
            self._db.update_sensor_data(bmc, sensor)
        except Exception as e:
            self._log.warning(f"Не удалось обновить данные сенсора [{bmc.address}][{sensor.name}]. Вызвано исключение: {e}")
        else:
            self._log.info(f"Данные сенсора [{bmc.address}][{sensor.name}] успешно обновлены.")

    def _db_insert_sensor_value(self, bmc: ConnectionData, sensor: Sensor):
        try:
            self._log.debug(f"Запись показаний сенсора [{bmc.address}][{sensor.name}].")
            self._db.insert_sensor_value(bmc, sensor)
        except Exception as e:
            self._log.warning(f"Не удалось записать показания сенсора [{bmc.address}][{sensor.name}]. Вызвано исключение: {e}")
        else:
            self._log.debug(f"Показания сенсора [{bmc.address}][{sensor.name}] успешно записаны.")

    def _ipmi_collect_sensors(self, bmc: ConnectionData) -> List[Sensor]:
        try:
            self._log.info(f"Сбор датчиков по адресу {bmc.address}")
            ipmi = self._ipmi(bmc)
            sensors = ipmi.collect()
        except Exception as e:
            self._log.error(f"Возникла ошибка при получении датчиков с устройства по адрессу {bmc.address}. Вызвано исключение: {e}")
        else:
            self._log.info(f"Сбор датчиков по адресу {bmc.address} завершен")
            return sensors

    def _db_get_sensors_control_info(self):
        try:
            self._log.info(f"Получение информации о контролируемых датчиках")
            control = self._db.get_sensors_control_info()
        except Exception as e:
            self._log.critical(f"Не удалось получить информацию о контролируемых датчиках. Вызвано исключение: {e}")
            sys.exit(1)
        else:
            self._log.info("Информация о контролируемых датчиках получена")
            return control

    def _db_get_ipmi_connections_data(self):
        try:
            self._log.debug(f"Получение данных всех bmc из базы данных")
            result = self._db.get_ipmi_connections_data()
        except Exception as e:
            self._log.critical(f"Не удалось получить данные bmc из базы данных. Вызвано исключение: {e}")
            sys.exit(1)
        return result


    def _sensor_data_check(self, bmc: ConnectionData, sensor: Sensor):
        if not self._cache.sensor_in_cache(bmc, sensor):
            self._db_insert_sensor_data(bmc, sensor)
        elif not self._cache.sensor_unchanged(bmc, sensor):
            self._db_update_sensor_data(bmc, sensor)

    def _record_bmc_sensors(self, bmc: ConnectionData):
        for sensor in self._ipmi_collect_sensors(bmc):
            self._sensor_data_check(bmc, sensor)
            if self._sensor_on_control(bmc, sensor):
                self._db_insert_sensor_value(bmc, sensor)

    def _get_sensors_control(self):
        self._control = self._db_get_sensors_control_info()

    def _sensor_on_control(self, bmc: ConnectionData, sensor: Sensor):
        if bmc.address in self._control:
            if sensor.name in self._control[bmc.address]:
                return self._control[bmc.address][sensor.name]
        return False
        

    def run(self):
        while True:
            print("start")

            BMCs = self._db_get_ipmi_connections_data()
            self._get_sensors_control()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self._record_bmc_sensors, BMCs)

            print("end")
            sleep(self._interval)
