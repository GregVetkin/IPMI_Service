from dataclasses import dataclass


@dataclass
class Sensor:
    name:   str     = None
    value:  str     = None
    unit:   str     = None
    status: str     = None
    lnr:    str     = None
    lc:     str     = None
    lnc:    str     = None
    unc:    str     = None
    uc:     str     = None
    unr:    str     = None


@dataclass
class ConnectionData:
    host:       str     = None
    username:   str     = None
    password:   str     = None

