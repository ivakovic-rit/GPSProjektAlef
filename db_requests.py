from tkinter import INSERT
import mysql.connector;
import gpxpy
import gpxpy.gpx


dbConnection = mysql.connector.connect(host='localhost', user='root', password='')
cursor = dbConnection.cursor(buffered=True)
goToDatabaseString = "USE gpx_daten"	
cursor.execute(goToDatabaseString)


def IsTrackInDatabase(fileName) -> bool:
    queryString = "SELECT * from track WHERE dateiname = '" + fileName + "'"
    cursor.execute(queryString)
    row_count = cursor.rowcount
    if (row_count == 0):
        print("Track nicht in Datenbank vorhanden")
        return False
    return True

def IsPersonInDatabase(name) -> bool:
    queryString = "SELECT * from person WHERE vorname = '" + name + "'"
    cursor.execute(queryString)
    row_count = cursor.rowcount
    if (row_count == 0):
        print("Person nicht in Datenbank vorhanden")
        return False
    return True

def IsVehicleInDatabase(licensePlateNumber) -> bool:
    queryString = "SELECT * from fahrzeug WHERE polKZ = '" + licensePlateNumber + "'"
    cursor.execute(queryString)
    row_count = cursor.rowcount
    if (row_count == 0):
        print("Fahrzeug nicht in Datenbank vorhanden")
        return False
    return True


def SavePersonToDb(name) -> int:
    if not (IsPersonInDatabase(name)):
        queryString = f"INSERT INTO `person` (`vorname`) VALUES ('{name}');"
        cursor.execute(queryString)
        dbConnection.commit()
        return cursor.lastrowid

def SaveVehicleToDb(licensePlateNumber) -> int:
    if not (IsVehicleInDatabase(licensePlateNumber)):
        queryString = f"INSERT INTO `fahrzeug` (`polKZ`) VALUES ('{licensePlateNumber}');"
        cursor.execute(queryString)
        dbConnection.commit()
        return cursor.lastrowid
    
def ImportRecordsToDB(gpxdatei, dateiname): 
    pid = 0
    fid = 0

    name = dateiname[0:2]
    licensePlateNumber = dateiname[3:11]

    if not (IsPersonInDatabase(name)):
        pid = SavePersonToDb(name)
    else: 
        queryString = f"SELECT pid FROM person WHERE vorname = '{name}'"
        cursor.execute(queryString)
        pid = cursor.fetchone()[0]
    
    if not (IsVehicleInDatabase(licensePlateNumber)):
        fid = SaveVehicleToDb(licensePlateNumber)
    
    else:
        queryString = f"SELECT fid FROM fahrzeug WHERE polKZ = '{licensePlateNumber}'"
        cursor.execute(queryString)
        fid = cursor.fetchone()[0]

    queryString = f"INSERT INTO `track` (`dateiname`, `pid`, `fid`) VALUES ('{dateiname}', {pid}, {fid});"
    cursor.execute(queryString)
    dbConnection.commit()
    tid = cursor.lastrowid

    gpx = gpxpy.parse(gpxdatei)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat = point.latitude
                lon = point.longitude
                ele = point.elevation
                datumZeit = ""
                if (point.time.year == None or point.time.month == None or point.time.day == None or point.time.hour == None or point.time.minute == None or point.time.second == None):
                    datumZeit = "0000-00-00 00:00:00"
                else: datumZeit = str(point.time.year) + "-" + str(point.time.month) + "-" + str(point.time.day) + " " + str(point.time.hour) + ":" + str(point.time.minute) + ":" + str(point.time.second)
                queryString = f"INSERT INTO `punkt` (`lat`, `lon`, `ele`, `datumZeit`, `tid`) VALUES ('{lat}', '{lon}', '{ele}', '{datumZeit}', '{tid}');"
                cursor.execute(queryString)
                dbConnection.commit()


def GetPunktDataFromDb(polkz, vonDatum, bisDatum) -> list:
    queryString = """
        SELECT p.lat, p.lon
        FROM fahrzeug f
        JOIN track t ON f.fid = t.fid
        JOIN punkt p ON t.tid = p.tid
        WHERE f.polKZ = %s
        AND (%s IS NULL OR p.datumZeit BETWEEN %s AND %s)
    """
    parameters = (polkz, vonDatum, vonDatum, bisDatum) if vonDatum and bisDatum else (polkz, None, None, None)
    cursor.execute(queryString, parameters)
    if (cursor.rowcount == 0):
        return []
    return cursor.fetchall()


def GetKfzPlatesFromDb() -> list: 
    queryString = f"SELECT polKZ FROM fahrzeug"
    cursor.execute(queryString)
    if (cursor.rowcount == 0):
        return []
    plates:list = cursor.fetchall()
    for i in range(len(plates)):
        plates[i] = plates[i][0].replace(" ", "")
    
    plates.insert(0, "Auswählen...")
    return plates