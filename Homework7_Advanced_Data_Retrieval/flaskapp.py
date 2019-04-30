import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from collections import OrderedDict

from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
 # connect_args needed to prevent thread error when exploring multiple pages without restarting the app for each page.
 # Reference https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa


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
    "<a href=/api/v1.0/precipitation>Precipitation Data for most recent year of observations</a><br/>"
    "<a href=/api/v1.0/stations> Station List: Name, ID</a><br/>"
    "<a href=/api/v1.0/tobs>Temperature Observation Data for most recent year of observations</a><br/>"
    "<br/>"
    "<p>/api/v1.0/yyyy-mm-dd<br/>Temperature Min Max Avg of all data starting from the prior year date of the users input.<br/> \
    Example: Input:2018-06-12, Data_Start:2017-06-12<br/> \
    !!!!! Requires start date input in format yyyy-mm-dd. Include the '-' character.</p><br/>"
    "<br/>"
    "<p>/api/v1.0/start/end<br/>Temperature Min Max Avg of all data starting from the prior year date of the users input, ending at user input end date from prior year.<br/> \
    Example: Input:2018-06-12, Data_Start:2017-06-12. The example also applies to end_date<br/> \
    !!!!! Requires start date input in format yyyy-mm-dd. Include the '-' character.</p><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    # Calculate the date 1 year ago from the last data point in the database
    most_current = session.query(Measurement.date).order_by(Measurement.date.desc()).first()  #last date/most recent observation 2017-08-23

    most_current = list(np.ravel(most_current)) # could not perform datetime operations on the returned query string with applying np.ravel.

    most_current =  dt.datetime.strptime(most_current[0], "%Y-%m-%d") # set string to datetime.obj
    yr_frm_moscurr = most_current.replace(year= most_current.year - 1)
    print(most_current)
    print(yr_frm_moscurr)

    # Perform a query to retrieve the data and precipitation scores
    year_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= yr_frm_moscurr).order_by(Measurement.date).all()
    precip_list = []
    for date,prcp in year_precip:
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

@app.route('/api/v1.0/tobs')
def tobs():
    # Calculate the date 1 year ago from the last data point in the database
    most_current = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #most_current #last date/most recent observation 2017-08-23
    most_current = list(np.ravel(most_current))
    most_current =  dt.datetime.strptime(most_current[0], "%Y-%m-%d")
    yr_frm_moscurr = most_current.replace(year= most_current.year - 1)
    #most_current
    #yr_frm_moscurr

    # Perform a query to retrieve the temperature observation data.
    year_precip = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= yr_frm_moscurr).order_by(Measurement.date).all()
    year_precip_list = []
    for date,tobs in year_precip:
        year_precip_dict = {}
        year_precip_dict[date] = tobs
        year_precip_list.append(year_precip_dict)

    return jsonify(year_precip_list)

@app.route('/api/v1.0/<start>')
def frm_strt_norm(start):

    def calc_temps(start_date):
        dt_start =  dt.datetime.strptime(start_date, "%Y-%m-%d") # set string to datetime.obj
        dt_st_prioryr = dt_start.replace(year= dt_start.year - 1)
        """TMIN, TAVG, and TMAX for a list of dates.

        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d

        Returns:
            TMIN, TAVE, and TMAX
        """

        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= dt_st_prioryr).all()

    year_norms = calc_temps(start)
    norms_list = []
    for min,avg,max in year_norms:
        norm_dict = {}
        norm_dict["Min Temp"] = min
        norm_dict["Avg Temp"] = avg
        norm_dict["Max Temp"] = max
        norms_list.append(norm_dict)

    return jsonify(norms_list)


@app.route('/api/v1.0/<start>/<end>')
def trip_norm(start,end):

    def calc_temps2(start_date,end_date):
        dt_start =  dt.datetime.strptime(start_date, "%Y-%m-%d") # set string to datetime.obj
        dt_end =  dt.datetime.strptime(end_date, "%Y-%m-%d") # set string to datetime.obj
        dt_st_prioryr = dt_start.replace(year= dt_start.year - 1)
        dt_end_prioryr = dt_end.replace(year= dt_end.year - 1)
        """TMIN, TAVG, and TMAX for a list of dates.

        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d

        Returns:
            TMIN, TAVE, and TMAX
        """

        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= dt_st_prioryr).filter(Measurement.date <= dt_end_prioryr).all()

    year_norms2 = calc_temps2(start,end)
    norms_list2 = []
    for min,avg,max in year_norms2:
        norm_dict = {}
        norm_dict["Min Temp"] = min
        norm_dict["Avg Temp"] = avg
        norm_dict["Max Temp"] = max
        norms_list2.append(norm_dict)

    return jsonify(norms_list2)






if __name__ == '__main__':
    app.run(debug=True)
