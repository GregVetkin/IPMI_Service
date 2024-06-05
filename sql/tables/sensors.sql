CREATE TABLE IPMI.SENSORS (
    id      SERIAL PRIMARY KEY,
    bmc_id  INT NOT NULL,
    name    VARCHAR(50),
    unit    VARCHAR(50),
    status  VARCHAR(50),
    lnr     FLOAT,
    lc      FLOAT,
    lnc     FLOAT,
    unc     FLOAT,
    uc      FLOAT,
    unr     FLOAT,
    FOREIGN KEY (bmc_id) REFERENCES IPMI.BMC(id)
);
