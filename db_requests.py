from tkinter import INSERT
import mysql.connector;
import gpxpy
import gpxpy.gpx


dbConnection = mysql.connector.connect(host='localhost', user='root', password='')
cursor = dbConnection.cursor(buffered=True)
goToDatabaseString = "USE gpx_daten"	
cursor.execute(goToDatabaseString)


def isTrackInDatabase(fileName) -> bool:
    queryString = "SELECT * from track WHERE dateiname = '" + fileName + "'"
    cursor.execute(queryString)
    row_count = cursor.rowcount
    if (row_count == 0):
        print("Track nicht in Datenbank vorhanden")
        return False
    return True

def isPersonInDatabase(name) -> bool:
    queryString = "SELECT * from person WHERE vorname = '" + name + "'"
    cursor.execute(queryString)
    row_count = cursor.rowcount
    if (row_count == 0):
        print("Person nicht in Datenbank vorhanden")
        return False
    return True

def isVehicleInDatabase(licensePlateNumber) -> bool:
    queryString = "SELECT * from fahrzeug WHERE polKZ = '" + licensePlateNumber + "'"
    cursor.execute(queryString)
    row_count = cursor.rowcount
    if (row_count == 0):
        print("Fahrzeug nicht in Datenbank vorhanden")
        return False
    return True


def savePersonToDb(name) -> int:
    if not (isPersonInDatabase(name)):
        queryString = f"INSERT INTO `person` (`vorname`) VALUES ('{name}');"
        cursor.execute(queryString)
        dbConnection.commit()
        return cursor.lastrowid

def saveVehicleToDb(licensePlateNumber) -> int:
    if not (isVehicleInDatabase(licensePlateNumber)):
        queryString = f"INSERT INTO `fahrzeug` (`polKZ`) VALUES ('{licensePlateNumber}');"
        cursor.execute(queryString)
        dbConnection.commit()
        return cursor.lastrowid
    
def saveTrackRecordToDb(gpxdatei, dateiname): 
    pid = 0
    fid = 0

    name = dateiname[0:2]
    licensePlateNumber = dateiname[3:11]

    if not (isPersonInDatabase(name)):
        pid = savePersonToDb(name)
    else: 
        queryString = f"SELECT pid FROM person WHERE vorname = '{name}'"
        cursor.execute(queryString)
        pid = cursor.fetchone()[0]
    
    if not (isVehicleInDatabase(licensePlateNumber)):
        fid = saveVehicleToDb(licensePlateNumber)
    
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
    queryString = f"SELECT fid FROM fahrzeug WHERE polKZ = '{polkz}'"
    cursor.execute(queryString)
    if (cursor.rowcount == 0):
        return []
    fid = cursor.fetchone()[0]
    queryString1 = f"SELECT tid FROM track WHERE fid = '{fid}'"
    cursor.execute(queryString1)
    if (cursor.rowcount == 0):
        return []
    tid = cursor.fetchone()[0]
    if vonDatum and bisDatum: queryString2 = f"SELECT lat, lon FROM punkt WHERE tid = '{tid}' and datumZeit BETWEEN '{vonDatum}' AND '{bisDatum}'"
    else: queryString2 = f"SELECT lat, lon FROM punkt WHERE tid = '{tid}'"
    cursor.execute(queryString2)
    if (cursor.rowcount == 0):
        return []
    return cursor.fetchall()


def getKfzPlatesFromDb() -> list: 
    queryString = f"SELECT polKZ FROM fahrzeug"
    cursor.execute(queryString)
    if (cursor.rowcount == 0):
        return []
    plates:list = cursor.fetchall()
    for i in range(len(plates)):
        plates[i] = plates[i][0].replace(" ", "")
    
    plates.insert(0, "Auswählen...")
    return plates