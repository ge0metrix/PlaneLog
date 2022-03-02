# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = aircraft_from_dict(json.loads(json_string))
#https://github.com/vradarserver/vrs/blob/c4b07e67cf48f4e246cb72a195d7767a3547d477/VirtualRadar.Database/BaseStation/Scripts/UpdateSchema.sql
import datetime
import json
from typing import List, Any, TypeVar, Callable, Type, cast
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    if (isinstance(x, int)):
        return x
    return None


def from_str(x: Any) -> str:
    if (isinstance(x, str)):
        return x
    return None


def from_bool(x: Any) -> bool:
    if (isinstance(x, bool)):
        return x
    return None


def from_float(x: Any) -> float:
    if (isinstance(x, (float,int) )):
        return float(x)
    return None


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if (isinstance(x, list)):
        return [f(y) for y in x]
    return None


def to_float(x: Any) -> float:
    if (isinstance(x, float)):
        return x
    return None


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

class Airline:
    icaocode: str
    itacode: str
    name: str
    country: str


class Aircraft:
    now: datetime.datetime
    hex: str
    type: str
    flight: str
    r: str
    t: str
    alt_baro: int
    ground: bool
    emergency: str
    category: str
    lat: float
    lon: float
    alert: int
    squawk: int


    def __init__(self, now: int, hex: str, type: str, flight: str, r: str, t: str, alt_baro: int, ground: bool, emergency: str, category: str, lat: float, lon: float, alert: int, squawk: int) -> None:
        self.now = now
        self.hex = hex
        self.type = type
        self.flight = flight
        self.r = r
        self.t = t
        self.alt_baro = alt_baro
        self.ground = ground
        self.emergency = emergency
        self.category = category
        self.lat = lat
        self.lon = lon
        self.alert = alert
        self.squawk = squawk

    
    def __str__(self)->str:
        return f"{str(self.hex)} \t {str(self.r): >6} \t {str(self.flight): >6} \t {str(self.now.isoformat(sep=' ', timespec='milliseconds'))} \t {str(self.t)} \t {str(self.squawk):0>4} \t Loc({str(self.lat)}, {str(self.lon)})"

    def isSeenBefore(self)->bool:
        return False


    @staticmethod
    def from_dict(obj: Any) -> 'Aircraft':
        try:
            assert isinstance(obj, dict)
            if(from_float(obj.get("now"))):
                now = datetime.datetime.fromtimestamp(from_float(obj.get("now")))
            elif(obj.get("now")):
                dateparser = dateutil.parser.parser()
                now = dateparser.parse(obj.get("now"))
            hex = from_str(obj.get("hex"))
            type = from_str(obj.get("type"))
            flight = from_str(obj.get("flight"))
            r = from_str(obj.get("r"))
            t = from_str(obj.get("t"))
            alt_baro = from_int(obj.get("alt_baro"))
            ground = from_bool(obj.get("ground"))
            emergency = from_str(obj.get("emergency"))
            category = from_str(obj.get("category"))
            lat = from_float(obj.get("lat"))
            lon = from_float(obj.get("lon"))
            alert = from_int(obj.get("alert"))
            squawk = obj.get("squawk")
        except Exception as e:
            print(e)
        return Aircraft(now, hex, type, flight, r, t, alt_baro, ground, emergency, category, lat, lon, alert, squawk)

    def to_dict(self) -> dict:
        result: dict = {}
        result["now"] = from_int(self.now)
        result["hex"] = from_str(self.hex)
        result["type"] = from_str(self.type)
        result["flight"] = from_str(self.flight)
        result["r"] = from_str(self.r)
        result["t"] = from_str(self.t)
        result["alt_baro"] = from_int(self.alt_baro)
        result["ground"] = from_bool(self.ground)
        result["emergency"] = from_str(self.emergency)
        result["category"] = from_str(self.category)
        result["lat"] = to_float(self.lat)
        result["lon"] = to_float(self.lon)
        result["alert"] = from_int(self.alert)
        result["squawk"] = from_int(self.squawk)
        return result


def aircraft_from_dict(s: Any) -> Aircraft:
    return Aircraft.from_dict(s)


def aircraft_to_dict(x: Aircraft) -> Any:
    return to_class(Aircraft, x)
