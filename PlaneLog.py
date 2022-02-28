import socket
import json
import os
import datetime
import sqlite3
import traceback
from Aircraft import Aircraft, aircraft_from_dict


TARHOST = os.environ.get("TARHOST","127.0.0.1")
TARPORT = int(os.environ.get("TARPORT",30047))
seen = {}

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
        A = aircraft_from_dict(msg)
        print(A)
    except Exception as e:
        print(e.with_traceback(None))
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TARHOST, TARPORT))
        f = s.makefile(mode="r",buffering=2048,encoding='ascii')
        while True:
            try:
                line = f.readline()
                if len(line)==0:
                    s.connect((TARHOST, TARPORT))
                
                msg = json.loads(line)
                
                if (msg.get("hex")) not in seen:
                    seen[msg.get("hex")] = datetime.datetime.now()
                    logAircraft(msg)
                    #print(json.dumps(msg, default=str))

                #print(len(seen))
            except Exception as e:
                print(e)
                print("----------------------")
                continue


if __name__=="__main__":
    main()