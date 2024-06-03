from dataclasses    import dataclass
from typing         import Union

@dataclass
class Sensor:
    name:   str                     = None
    value:  Union[float, None]      = None
    unit:   Union[str, None]        = None
    status: Union[str, None]        = None
    lnr:    Union[float, None]      = None
    lc:     Union[float, None]      = None
    lnc:    Union[float, None]      = None
    unc:    Union[float, None]      = None
    uc:     Union[float, None]      = None
    unr:    Union[float, None]      = None


@dataclass
class ConnectionData:
    address:    str     = None
    username:   str     = None
    password:   str     = None

