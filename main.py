import gpxpy
import gpxpy.gpx
import os
from flask import Flask
from db_requests import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def main():
    counter = 0
    directory = "gpx-Dateien"
    for filename in os.listdir(directory):
        if not filename.endswith(".gpx") or isTrackInDatabase(filename): continue
        gpx_file = open(directory + "/" + filename, 'r')
        saveTrackRecordToDb(gpx_file, filename)
        counter += 1

    print(f'Anzahl der Dateien: {counter}')

if __name__ == '__main__':
    main()