import gpxpy
import gpxpy.gpx
import os
from flask import Flask, request, render_template
import folium
from db_requests import *

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    path_points = []
    map_file = "./static/path_only_map.html"
    shouldshowIframe = False
    kfzPlates:list = getKfzPlatesFromDb()
    
    if request.method == 'POST':
        name = request.form.get('name')
        kfz = request.form.get('kfz')
        von_datum = request.form.get('von_datum')
        bis_datum = request.form.get('bis_datum')

        print(f'Name: {name}, KFZ: {kfz}, Von Datum: {von_datum}, Bis Datum: {bis_datum}')
        path_points: list = GetPunktDataFromDb(kfz, von_datum, bis_datum)
        if path_points.count == 0: shouldshowIframe = False
        else: shouldshowIframe = True
        m = folium.Map(location=path_points[0], zoom_start=12)

        path = folium.PolyLine(locations=path_points, color='blue', weight=5)
        path.add_to(m)

        m.save(map_file)

    return render_template('index.html', map_file=map_file, shouldshowIframe=shouldshowIframe, kfzPlates = kfzPlates)


if __name__ == '__main__':
    app.run(debug=True)

# def main():
#     counter = 0
#     directory = "gpx-Dateien"
#     for filename in os.listdir(directory):
#         if not filename.endswith(".gpx") or isTrackInDatabase(filename): continue
#         gpx_file = open(directory + "/" + filename, 'r')
#         saveTrackRecordToDb(gpx_file, filename)
#         counter += 1

#     print(f'Anzahl der Dateien: {counter}')

# if __name__ == '__main__':
#     main()