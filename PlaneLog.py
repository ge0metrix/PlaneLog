import asyncio
from TarConn import tarConn
import time
import json
import Aircraft
import DdHelper
import datetime
import os

seen = {}
async def lookupAirline(flight):
    pass

async def main():
    db = DdHelper.db_helper("PlaneLog.db")
    incon = tarConn(TARHOST, TARPORT)

    while True:

    #time.sleep(0.3)
        try:
            lines = await asyncio.wait_for(incon.readlines(), 10)
            
            if lines == "closed":
                time.sleep(0.2)
                continue

            for line in lines:
                record=json.loads(line)
                A = Aircraft.aircraft_from_dict(record)
                #reduce thrash by waiting 10 seconds between writes for a given aircraft icao
                if not seen.get(record.get("hex")) or seen.get(record.get("hex")) <= (datetime.datetime.now() - datetime.timedelta(seconds=10)) :
                    db.upsertAircraft(A)
                    seen[record.get("hex")]=datetime.datetime.now()
        except asyncio.TimeoutError:
            print(f'readlines timeout')
            await incon.connect()
        

TARHOST = os.environ.get("TARHOST","127.0.0.1")
TARPORT = int(os.environ.get("TARPORT",30047))
asyncio.run(main())