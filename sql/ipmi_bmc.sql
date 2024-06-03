CREATE TABLE IPMI.BMC (
    id          SERIAL PRIMARY KEY,
    address     VARCHAR(255) NOT NULL,
    username    VARCHAR(255) NOT NULL,
    password    VARCHAR(255) NOT NULL
);
