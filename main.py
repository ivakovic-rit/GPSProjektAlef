import gpxpy
import gpxpy.gpx
import os
from flask import Flask, request, render_template
from db_requests import *

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        kfz = request.form.get('kfz')
        von_datum = request.form.get('von_datum')
        bis_datum = request.form.get('bis_datum')
        # You can perform any logic or processing with these values here
        
        # For now, just printing them to the console
        print(f'Name: {name}, KFZ: {kfz}, Von Datum: {von_datum}, Bis Datum: {bis_datum}')
    
    return render_template('index.html')

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