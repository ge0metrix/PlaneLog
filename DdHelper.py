import datetime
import os
from pickle import FALSE
import sqlite3
import Aircraft
from sqlite3 import Error
import requests
import csv
from io import StringIO



DBInitSQL = """
DROP TABLE IF EXISTS Airlines;
CREATE TABLE Airlines (
    ICAO     VARCHAR (3),
    Name     VARCHAR (50),
    Callsign VARCHAR (50),
    Country  VARCHAR (100),
    IATA     VARCHAR (3),
    PRIMARY KEY (
        ICAO
    )
);

DROP TABLE IF EXISTS PlaneLog;
CREATE TABLE PlaneLog (
    ICAO         STRING (6)   NOT NULL,
    FirstSeen    DATETIME,
    LastSeen     DATETIME,
    Registration VARCHAR (20),
    TypeCode     VARCHAR (10),
    Flight       VARCHAR (20),
    Squawk INT,
    PRIMARY KEY (
        ICAO
    )
);

DROP TABLE IF EXISTS FlightLog;
CREATE TABLE FlightLog (
    ICAO VARCHAR(6) NOT NULL,
    FLIGHT VARCHAR(20),
    LogDate DATETIME
);

DROP TABLE IF EXISTS SquawkLog;
CREATE TABLE SquawkLog (
    ICAO VARCHAR(6) NOT NULL,
    Squawk INT,
    LogDate DATETIME
);

CREATE TRIGGER logFlights 
AFTER UPDATE ON PlaneLog 
WHEN (NEW.Flight <> OLD.Flight AND NEW.Flight IS NOT NULL)
BEGIN
    INSERT INTO FlightLog (ICAO, Flight, LogDate) VALUES (NEW.ICAO, OLD.Flight, DATETIME('NOW'));
END;

CREATE TRIGGER logSquawks 
AFTER UPDATE ON PlaneLog 
WHEN (NEW.Squawk <> OLD.Squawk AND NEW.Squawk IS NOT NULL)
BEGIN
    INSERT INTO SquawkLog (ICAO, Squawk, LogDate) VALUES (NEW.ICAO, OLD.Squawk, DATETIME('NOW'));
END;

"""
class db_helper():
    conn: sqlite3.Connection
    def __init__(self, sqldbpath, reinit=False):
        try:
            if(not os.path.exists(sqldbpath) or reinit):
                self.conn = sqlite3.connect(sqldbpath)
                cur=self.conn.cursor()
                cur.executescript(DBInitSQL)
                self.conn.commit()
                cur.close()
                r = requests.get("https://raw.githubusercontent.com/kx1t/planefence-airlinecodes/main/airlinecodes.txt")
                print(r.text)
                rdr = csv.reader(r.text.splitlines())
                for r in rdr:
                    #print(r)
                    cur = self.conn.cursor()
                    query = "INSERT INTO Airlines (ICAO, Name, Callsign, Country) VALUES (?, ?, ?, ?)"
                    cur.execute(query,r)
                    self.conn.commit()
                    cur.close()

    
            else:
                self.conn=sqlite3.connect(sqldbpath)
        except sqlite3.Error as sqlErr:
            print(sqlErr)

    def getAircraft(self, aircraft:Aircraft.Aircraft) -> Aircraft.Aircraft:
        if(not self.conn):
            print("YIKES!")
            raise Exception("YIKES!")
        query:str = "SELECT ICAO, LastSeen, Registration, Flight, Squawk FROM PlaneLog WHERE ICAO=:hex ORDER BY LastSeen DESC LIMIT 1;"
        cur = self.conn.cursor()
        queryparams = {'hex':str(aircraft.hex.lower())}
        try:
            cur.execute(query, queryparams)
        except Error as e:
            print(e)
            pass

        row = cur.fetchone()
        if row:
            #print(row)
            x = {"hex":row[0], "now":row[1], "r":row[2], "t":row[3], "squawk":row[4]}
            #print(x)   
            A = Aircraft.aircraft_from_dict(x)
            return A
        return None

    def upsertAircraft(self, aircraft:Aircraft.Aircraft):
        #Check if we've seen the aircraft before
        A = self.getAircraft(aircraft)
        if(not A):
            print("INSERTING:\t{}".format(aircraft))
            query = "INSERT INTO PlaneLog (ICAO, FirstSeen, LastSeen, Registration, TypeCode, Flight, Squawk) VALUES (?, ?, ?, ?, ?, ?,?)"
            cur =self.conn.cursor()
            data = (aircraft.hex, aircraft.now, aircraft.now, aircraft.r, aircraft.t, aircraft.flight, aircraft.squawk)
            cur.execute(query, data)
            self.conn.commit()
        else:
            #print("{} < {}".format(A.now, (datetime.datetime.now() - datetime.timedelta(minutes=1)) ))
            print("UPDATING:\t{}".format(aircraft))
            query = "UPDATE PlaneLog SET LastSeen = ?, Registration = ?, Squawk = ?, Flight = ? WHERE ICAO = ? "
            cur = self.conn.cursor()
            data = (datetime.datetime.now(), aircraft.r, aircraft.squawk, aircraft.flight, aircraft.hex )
            cur.execute(query, data)
            self.conn.commit()

