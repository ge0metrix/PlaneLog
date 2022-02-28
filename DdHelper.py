import sqlite3
import Aircraft
from sqlite3 import Error

class db_helper():
    conn: sqlite3.Connection
    def __init__(self, sqldbpath):
        try:
            self.conn = sqlite3.connect(sqldbpath)
        except sqlite3.Error as sqlErr:
            print(sqlErr)

    def getAircraft(self, icao:str) -> Aircraft:
        #query = "SELECT ModeS, LastModified, Registration, ICAOTypeCode, Type FROM Aircraft WHERE ModeS = ?"
        if(not self.conn):
            print("YIKES!")
            return
        query:str = "SELECT * FROM PlaneLog WHERE ICAO=:hex;"
        cur = self.conn.cursor()
        print(query)
        queryparams = {'hex':str(icao.lower())}
        try:
            cur.execute(query, queryparams)
        except Error as e:
            print(e)
            pass
        print(cur.rowcount)
        if cur.rowcount > 0:
            row = cur.fetchone()
            x = {"hex":row[0], "now":row[1], "r":row[2], "t":row[3]}
            A = Aircraft.aircraft_from_dict(x)
            return A
        return None

    def upsertAircraft(self, aircraft:Aircraft.Aircraft):
        if(self.getAircraft(aircraft.hex) == None):
            query = "INSERT INTO PlaneLog (ICAO, FirstSeen, LastSeen, Registration, TypeCode) VALUES (?, ?, ?, ?, ?)"
            cur =self.conn.cursor()
            data = (aircraft.hex, aircraft.now, aircraft.now, aircraft.r, aircraft.t)
            cur.execute(query, data)
            self.conn.commit()
        else:
            query = "UPDATE PlaneLog SET LastSeen = ?, Registration = ? WHERE ICAO = ?"
            cur = self.conn.cursor()
            data = (aircraft.now, aircraft.r, aircraft.hex)
            cur.execute(query, data)
            self.conn.commit()