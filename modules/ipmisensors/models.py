from dataclasses import dataclass


@dataclass
class IPMISernsor:
    name:   str
    value:  str
    unit:   str
    status: str
    lnr:    str
    lc:     str
    lnc:    str
    unc:    str
    uc:     str
    unr:    str


@dataclass
class IPMIConnectionData:
    host:       str
    username:   str
    password:   str

