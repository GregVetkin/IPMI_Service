CREATE TABLE IPMI.BMC (
    id          SERIAL PRIMARY KEY,
    address     VARCHAR(15) NOT NULL UNIQUE,
    username    VARCHAR(50) NOT NULL,
    password    VARCHAR(50) NOT NULL
);
