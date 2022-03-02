import datetime
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
    
    def initDB():
        pass
    
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


"""

DROP TABLE PlaneLog;
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

DROP TABLE FlightLog;
CREATE TABLE FlightLog (
    ICAO VARCHAR(6) NOT NULL,
    FLIGHT VARCHAR(20),
    LogDate DATETIME
);

DROP TABLE SquawkLog;
CREATE TABLE SquawkLog (
    ICAO VARCHAR(6) NOT NULL,
    Squawk INT,
    LogDate DATETIME
);

CREATE TRIGGER logFlights 
AFTER UPDATE ON PlaneLog 
WHEN (NEW.Flight <> OLD.Flight AND NEW.Flight IS NOT NULL) OR (OLD.Flight IS NULL AND NEW.Flight IS NOT NULL)
BEGIN
    INSERT INTO FlightLog (ICAO, Flight, LogDate) VALUES (NEW.ICAO, OLD.Flight, DATETIME('NOW'));
END;

CREATE TRIGGER logSquawks 
AFTER UPDATE ON PlaneLog 
WHEN (NEW.Squawk <> OLD.Squawk AND NEW.Squawk IS NOT NULL) OR (OLD.Squawk IS NULL AND NEW.Squawk IS NOT NULL)
BEGIN
    INSERT INTO SquawkLog (ICAO, Squawk, LogDate) VALUES (NEW.ICAO, OLD.Squawk, DATETIME('NOW'));
END;

"""