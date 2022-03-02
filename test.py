import sqlite3


conn = sqlite3.connect("BaseStation.sqb")
cur = conn.cursor()
query = "SELECT * FROM PlaneLog WHERE ICAO = :hex;"
cur.execute(query, {'hex':'3c70c9'})
rows = cur.fetchall()
print(cur.rowcount)
print(cur)
for row in rows:
    print(row)