CREATE TABLE IPMI.SENSORS_CONTROL (
    id          SERIAL PRIMARY KEY,
    sensor_id   INT NOT NULL,
    control     BOOLEAN,
    FOREIGN KEY (sensor_id) REFERENCES IPMI.SENSORS(id)
);


# Функция для добавления нового сенсора на контроль

CREATE OR REPLACE FUNCTION add_sensor_control()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO IPMI.SENSORS_CONTROL (sensor_id, control)
    VALUES (NEW.id, TRUE);  -- Можно установить значение по умолчанию для control
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


# Триггер для таблицы IPMI.SENSORS
CREATE TRIGGER after_sensor_insert
AFTER INSERT ON IPMI.SENSORS
FOR EACH ROW
EXECUTE FUNCTION add_sensor_control();
