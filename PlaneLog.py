import socket
import json
import os
import datetime
import sqlite3
import Aircraft
from DdHelper import db_helper



TARHOST = os.environ.get("TARHOST","127.0.0.1")
TARPORT = int(os.environ.get("TARPORT",30047))
TIMEOUT = 3600
seen = {}
db:db_helper = None

"""
Setup DB Connection
"""
def getDb(): 
    pass


"""
Cast msg to Aircraft and call ToDb()
"""
def logAircraft(msg):
    try:
        A = Aircraft.aircraft_from_dict(msg)
        print(A)
        return A
    except Exception as e:
        print(e)
    pass

"""
Check DB if we've seen this aircraft
"""
def isSeen():
    pass

"""
Update the Airctaft record in the DB if we've seen it
(mostly lastSeenDate)
"""
def UpdateAircraft(msg):
    pass


def main():
    db = db_helper("BaseStation.sqb")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TARHOST, TARPORT))
        f = s.makefile(mode="r",buffering=2048,encoding='ascii')
        while True:
            try:
                line = f.readline()
                if len(line)==0: #disconnect? reconnect!
                    s.connect((TARHOST, TARPORT))
                
                msg = json.loads(line)
                #not seen yet? add it to see, and parse it.
                if (msg.get("hex")) not in seen:
                    seen[msg.get("hex")] = datetime.datetime.now()
                    logAircraft(msg)
                    A = db.getAircraft(msg.get("hex"))
                    db.upsertAircraft(logAircraft(msg))
                    print(A)
                #cleanup aircraft not seen in the TIMEOUT period, no need to keep them in memory.
                for k,v in list(seen.items()):
                    if v <= datetime.datetime.now() - datetime.timedelta(minutes=TIMEOUT):
                         x=seen.pop(k)
                         #print(k, x)
            except Exception as e:
                print(e)
                #print("----------------------")
                continue


if __name__=="__main__":
    main()