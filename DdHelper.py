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

    def getAircraft(self, aircraft:Aircraft.Aircraft) -> Aircraft.Aircraft:
        #query = "SELECT ModeS, LastModified, Registration, ICAOTypeCode, Type FROM Aircraft WHERE ModeS = ?"
        if(not self.conn):
            print("YIKES!")
            return
        query:str = "SELECT * FROM PlaneLog WHERE ICAO=:hex and Flight=:flight;"
        cur = self.conn.cursor()
        #print(query)
        queryparams = {'hex':str(aircraft.hex.lower()), "flight":aircraft.flight}
        try:
            cur.execute(query, queryparams)
        except Error as e:
            print(e)
            pass

        row = cur.fetchone()
        if row:
            #print(row)
            x = {"hex":row[0], "now":row[1], "r":row[2], "t":row[3]}
            #print(x)   
            A = Aircraft.aircraft_from_dict(x)
            return A
        return None

    def upsertAircraft(self, aircraft:Aircraft.Aircraft):
        if(self.getAircraft(aircraft) == None):
            print("INSERTING:\t{}".format(aircraft))
            query = "INSERT INTO PlaneLog (ICAO, FirstSeen, LastSeen, Registration, TypeCode, Flight) VALUES (?, ?, ?, ?, ?, ?)"
            cur =self.conn.cursor()
            data = (aircraft.hex, aircraft.now, aircraft.now, aircraft.r, aircraft.t, aircraft.flight)
            cur.execute(query, data)
            self.conn.commit()
        else:
            print("UPDATING:\t{}".format(aircraft))
            query = "UPDATE PlaneLog SET LastSeen = ?, Registration = ? WHERE ICAO = ? and Flight = ?"
            cur = self.conn.cursor()
            data = (aircraft.now, aircraft.r, aircraft.hex, aircraft.flight)
            cur.execute(query, data)
            self.conn.commit()

"""
CREATE TABLE PlaneLog (
    ICAO         STRING (6)   NOT NULL,
    FirstSeen    DATETIME,
    LastSeen     DATETIME,
    Registration VARCHAR (20),
    TypeCode     VARCHAR (10),
    Flight       VARCHAR (20),
    PRIMARY KEY (
        ICAO,
        Flight
    )
);

"""