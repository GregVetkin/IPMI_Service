CREATE OR REPLACE FUNCTION add_sensor_control()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO IPMI.SENSORS_CONTROL (sensor_id, control)
    VALUES (NEW.id, FALSE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


