from typing import Optional
from flask import Flask, jsonify, render_template, Response
import wmi

import datetime, os

app = Flask(__name__)
w = wmi.WMI(namespace = r"root\wmi")

def get_temp(property: str) -> Optional[int]:
    try:
        w_class = w.MSAcpi_ThermalZoneTemperature()[0]
        temp = getattr(w_class,property,None)
    except Exception as e: # this is bad practice, TODO: isolate exception types
        temp = None
        print('get_temp error',e)

    # convert from deci-degrees Kelvin to deci-degrees Celcius
    if not temp is None:
        temp = temp - 2732
    return temp

@app.route('/')
def index() -> str:
    return render_template('index.html.j2')

@app.route('/current-temp')
def get_current_temp() -> Response:
    temp = get_temp('CurrentTemperature')
    dt = datetime.datetime.now()
    current_temp = {'datetime': str(dt), 'temp': temp}    
    return jsonify(current_temp)

@app.route('/trip-points')
def get_trip_point() -> Response:
    class_properties = ['ActiveTripPoint','PassiveTripPoint','CriticalTripPoint']    
    trip_points = {property: get_temp(property) for property in class_properties}
    return jsonify(trip_points)

if __name__ == '__main__':
    debug = False # use True for integration testing, TODO: move to .env
    if debug:
        from tests.mockforWMI import MockWMI
        w = MockWMI(namespace = 'test WMI')
    app.run(host = '127.0.0.1', port = 4999, debug = debug)