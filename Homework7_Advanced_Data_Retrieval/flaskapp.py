import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from collections import OrderedDict

from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Set up Flask app
app = Flask(__name__)

#### Flask routes

@app.route("/")
def welcome():
    #List all available api routes.
    return(
    f"Available routes:<br/>"
    "<a href=/api/v1.0/precipitation> click here</a>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    year_precip = session.query(Measurement.station, Measurement.prcp,Measurement.date).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    precip_list = []
    for station,prcp,date in year_precip:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_list.append(precip_dict)

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    stations = session.query(Station.name,Station.id).all()
    station_list = list(np.ravel(stations))
    return jsonify(station_list)

    # for name,id in stations:
    #     station_dict = {}
    #     station_dict["Name"] = name
    #     station_dict["Station ID"] = id
    #     station_list.append(station_dict)
    # return jsonify(station_list)


if __name__ == '__main__':
    app.run(debug=True)
