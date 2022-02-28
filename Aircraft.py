# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = aircraft_from_dict(json.loads(json_string))
import datetime
import json
from typing import List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
#    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
#    assert isinstance(x, str)
    if (isinstance(x, str)):
        return x
    return None


def from_bool(x: Any) -> bool:
#    assert isinstance(x, bool)
    if (isinstance(x, bool)):
        return x
    return None


def from_float(x: Any) -> float:
#    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    if (isinstance(x, (float,int) )):
        return float(x)
    return None


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
#    assert isinstance(x, list)
    if (isinstance(x, list)):
        return [f(y) for y in x]
    return None


def to_float(x: Any) -> float:
#    assert isinstance(x, float)
    if (isinstance(x, float)):
        return x
    return None


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Aircraft:
    now: datetime
    hex: str
    type: str
    flight: str
    r: str
    t: str
    alt_baro: int
    ground: bool
    alt_geom: int
    gs: float
    ias: int
    tas: int
    mach: float
    wd: int
    ws: int
    oat: int
    tat: int
    track: float
    track_rate: float
    roll: float
    mag_heading: float
    true_heading: float
    baro_rate: int
    geom_rate: int
    emergency: str
    category: str
    nav_qnh: float
    nav_altitude_mcp: int
    nav_modes: List[str]
    lat: float
    lon: float
    nic: int
    rc: int
    seen_pos: int
    version: int
    nic_baro: int
    nac_p: int
    nac_v: int
    sil: int
    sil_type: str
    gva: int
    sda: int
    alert: int
    squawk: int
    spi: int
    mlat: List[Any]
    tisb: List[Any]
    messages: int
    seen: int
    rssi: float

    def __init__(self, now: int, hex: str, type: str, flight: str, r: str, t: str, alt_baro: int, ground: bool, alt_geom: int, gs: float, ias: int, tas: int, mach: float, wd: int, ws: int, oat: int, tat: int, track: float, track_rate: float, roll: float, mag_heading: float, true_heading: float, baro_rate: int, geom_rate: int, emergency: str, category: str, nav_qnh: float, nav_altitude_mcp: int, nav_modes: List[str], lat: float, lon: float, nic: int, rc: int, seen_pos: int, version: int, nic_baro: int, nac_p: int, nac_v: int, sil: int, sil_type: str, gva: int, sda: int, alert: int, squawk: int, spi: int, mlat: List[Any], tisb: List[Any], messages: int, seen: int, rssi: float) -> None:
        self.now = now
        self.hex = hex
        self.type = type
        self.flight = flight
        self.r = r
        self.t = t
        self.alt_baro = alt_baro
        self.ground = ground
        self.alt_geom = alt_geom
        self.gs = gs
        self.ias = ias
        self.tas = tas
        self.mach = mach
        self.wd = wd
        self.ws = ws
        self.oat = oat
        self.tat = tat
        self.track = track
        self.track_rate = track_rate
        self.roll = roll
        self.mag_heading = mag_heading
        self.true_heading = true_heading
        self.baro_rate = baro_rate
        self.geom_rate = geom_rate
        self.emergency = emergency
        self.category = category
        self.nav_qnh = nav_qnh
        self.nav_altitude_mcp = nav_altitude_mcp
        self.nav_modes = nav_modes
        self.lat = lat
        self.lon = lon
        self.nic = nic
        self.rc = rc
        self.seen_pos = seen_pos
        self.version = version
        self.nic_baro = nic_baro
        self.nac_p = nac_p
        self.nac_v = nac_v
        self.sil = sil
        self.sil_type = sil_type
        self.gva = gva
        self.sda = sda
        self.alert = alert
        self.squawk = squawk
        self.spi = spi
        self.mlat = mlat
        self.tisb = tisb
        self.messages = messages
        self.seen = seen
        self.rssi = rssi
    
    def __str__(self)->str:
        return f"{str(self.hex)} \t {str(self.r): >6} \t {str(self.flight): >6} \t {str(self.now)} \t {str(self.t)} \t {str(self.squawk):0>4} \t Loc({str(self.lat)}, {str(self.lon)})"

    def isSeenBefore(self)->bool:
        return False


    @staticmethod
    def from_dict(obj: Any) -> 'Aircraft':
        try:
            assert isinstance(obj, dict)
            now = datetime.datetime.fromtimestamp(from_float(obj.get("now")))
            hex = from_str(obj.get("hex"))
            type = from_str(obj.get("type"))
            flight = from_str(obj.get("flight"))
            r = from_str(obj.get("r"))
            t = from_str(obj.get("t"))
            alt_baro = from_int(obj.get("alt_baro"))
            ground = from_bool(obj.get("ground"))
            alt_geom = from_int(obj.get("alt_geom"))
            gs = from_float(obj.get("gs"))
            ias = from_int(obj.get("ias"))
            tas = from_int(obj.get("tas"))
            mach = from_float(obj.get("mach"))
            wd = from_int(obj.get("wd"))
            ws = from_int(obj.get("ws"))
            oat = from_int(obj.get("oat"))
            tat = from_int(obj.get("tat"))
            track = from_float(obj.get("track"))
            track_rate = from_float(obj.get("track_rate"))
            roll = from_float(obj.get("roll"))
            mag_heading = from_float(obj.get("mag_heading"))
            true_heading = from_float(obj.get("true_heading"))
            baro_rate = from_int(obj.get("baro_rate"))
            geom_rate = from_int(obj.get("geom_rate"))
            emergency = from_str(obj.get("emergency"))
            category = from_str(obj.get("category"))
            nav_qnh = from_float(obj.get("nav_qnh"))
            nav_altitude_mcp = from_int(obj.get("nav_altitude_mcp"))
            nav_modes = from_list(from_str, obj.get("nav_modes"))
            lat = from_float(obj.get("lat"))
            lon = from_float(obj.get("lon"))
            nic = from_int(obj.get("nic"))
            rc = from_int(obj.get("rc"))
            seen_pos = from_int(obj.get("seen_pos"))
            version = from_int(obj.get("version"))
            nic_baro = from_int(obj.get("nic_baro"))
            nac_p = from_int(obj.get("nac_p"))
            nac_v = from_int(obj.get("nac_v"))
            sil = from_int(obj.get("sil"))
            sil_type = from_str(obj.get("sil_type"))
            gva = from_int(obj.get("gva"))
            sda = from_int(obj.get("sda"))
            alert = from_int(obj.get("alert"))
            squawk = from_int(obj.get("squawk"))
            spi = from_int(obj.get("spi"))
            mlat = from_list(lambda x: x, obj.get("mlat"))
            tisb = from_list(lambda x: x, obj.get("tisb"))
            messages = from_int(obj.get("messages"))
            seen = from_int(obj.get("seen"))
            rssi = from_float(obj.get("rssi"))
        except Exception as e:
            print(e)
        return Aircraft(now, hex, type, flight, r, t, alt_baro, ground, alt_geom, gs, ias, tas, mach, wd, ws, oat, tat, track, track_rate, roll, mag_heading, true_heading, baro_rate, geom_rate, emergency, category, nav_qnh, nav_altitude_mcp, nav_modes, lat, lon, nic, rc, seen_pos, version, nic_baro, nac_p, nac_v, sil, sil_type, gva, sda, alert, squawk, spi, mlat, tisb, messages, seen, rssi)

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
        result["alt_geom"] = from_int(self.alt_geom)
        result["gs"] = to_float(self.gs)
        result["ias"] = from_int(self.ias)
        result["tas"] = from_int(self.tas)
        result["mach"] = to_float(self.mach)
        result["wd"] = from_int(self.wd)
        result["ws"] = from_int(self.ws)
        result["oat"] = from_int(self.oat)
        result["tat"] = from_int(self.tat)
        result["track"] = to_float(self.track)
        result["track_rate"] = to_float(self.track_rate)
        result["roll"] = to_float(self.roll)
        result["mag_heading"] = to_float(self.mag_heading)
        result["true_heading"] = to_float(self.true_heading)
        result["baro_rate"] = from_int(self.baro_rate)
        result["geom_rate"] = from_int(self.geom_rate)
        result["emergency"] = from_str(self.emergency)
        result["category"] = from_str(self.category)
        result["nav_qnh"] = to_float(self.nav_qnh)
        result["nav_altitude_mcp"] = from_int(self.nav_altitude_mcp)
        result["nav_modes"] = from_list(from_str, self.nav_modes)
        result["lat"] = to_float(self.lat)
        result["lon"] = to_float(self.lon)
        result["nic"] = from_int(self.nic)
        result["rc"] = from_int(self.rc)
        result["seen_pos"] = from_int(self.seen_pos)
        result["version"] = from_int(self.version)
        result["nic_baro"] = from_int(self.nic_baro)
        result["nac_p"] = from_int(self.nac_p)
        result["nac_v"] = from_int(self.nac_v)
        result["sil"] = from_int(self.sil)
        result["sil_type"] = from_str(self.sil_type)
        result["gva"] = from_int(self.gva)
        result["sda"] = from_int(self.sda)
        result["alert"] = from_int(self.alert)
        result["squawk"] = from_int(self.squawk)
        result["spi"] = from_int(self.spi)
        result["mlat"] = from_list(lambda x: x, self.mlat)
        result["tisb"] = from_list(lambda x: x, self.tisb)
        result["messages"] = from_int(self.messages)
        result["seen"] = from_int(self.seen)
        result["rssi"] = to_float(self.rssi)
        return result


def aircraft_from_dict(s: Any) -> Aircraft:
    return Aircraft.from_dict(s)


def aircraft_to_dict(x: Aircraft) -> Any:
    return to_class(Aircraft, x)
