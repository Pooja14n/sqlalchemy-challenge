# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlite3



import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# conn = sqlite3.connect("sqlite:///C:\\Users\\sridh\\OneDrive\\Documents\\GitHub\\sqlalchemy-challenge\\SurfsUp\\Resources\\hawaii.sqlite")
# curr = conn.cursor()
engine = create_engine("sqlite:///C:\\Users\\sridh\\OneDrive\\Documents\\GitHub\\sqlalchemy-challenge\\SurfsUp\\Resources\\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# 1. "/"
@app.route("/")
def homepage(): 
    return (f"Honolulu, Hawaii Climate Analysis! <br>"
            f"Available Routes: <br>"
            f"/api/v1.0/precipitation <br>"
            f"/api/v1.0/stations <br>"
            f"/api/v1.0/tobs <br>"
            f"/api/v1.0/start <br>"
            f"/api/v1.0/start/end"
    )
    
    
# 2. "/api/v1.0/precipitation"
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(measurement.date, measurement.prcp).all()

    prcp_results = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_results.append(prcp_dict) 

    session.close()
    return jsonify(prcp_results)

# 3. "/api/v1.0/stations"
@app.route("/api/v1.0/stations")
def stations():
    
          
    results1 = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
        
    station_res = []
    for station, name, latitude, longitude, elevation in results1:
        station_dict = {}
        #station_dict[Id] = id
        station_dict[station] = station
        station_dict[name] = name
        station_dict[latitude] = latitude
        station_dict[longitude] = longitude
        station_dict[elevation] = elevation
        station_res.append(station_dict)
    
    session.close()
    stations = list(np.ravel(results1))
    return jsonify(stations)



# 4. "/api/v1.0/tobs"
@app.route("/api/v1.0/tobs")
def tobs():
    
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]
    
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    last_dt = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
    one_year_date = last_dt - dt.timedelta(days=365)

    active_tobs = session.query(measurement.date, measurement.tobs).filter((measurement.station == active_stations) & (measurement.date >= one_year_date) & (measurement.date <= last_dt)).all()

    session.close()
    tobs = list(np.ravel(active_tobs))
    return jsonify(tobs)


# 5(a) "/api/v1.0/<start>"  
@app.route("/api/v1.0/<start>")
def start_date(start):
    
    starting_date = dt.datetime.strptime(start,'%Y-%m-%d').date()
    results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= starting_date).group_by(measurement.date).all()

    
    # start_date_list = []
    # for date, tmin, tavg, tmax in results:
    #     start_dict = {}
    #     start_dict['Date'] = date
    #     start_dict['TMIN'] = tmin
    #     start_dict['TAVG'] = tavg
    #     start_dict['TMAX'] = tmax
    #     start_date_list.append(start_dict)

    
    session.close()
    start_dt = list(np.ravel(results))
    return jsonify(start_dt)



# 5(b) "/api/v1.0/<start>/<end>"  
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
   
    
    starting_date = dt.datetime.strptime(start,'%Y-%m-%d').date()
    ending_date = dt.datetime.strptime(end,'%Y-%m-%d').date()
    
    results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= starting_date).filter(measurement.date <= ending_date).group_by(measurement.date).all()

    # start_end_list = []
    # for date, tmin, tmax, tavg in results:
    #     start_end_dict = {}
    #     start_end_dict['Date'] = date
    #     start_end_dict['TMIN'] = tmin
    #     start_end_dict['TMAX'] = tmax
    #     start_end_dict['TAVG'] = tavg
    #     start_end_list.append(start_end_dict)

    
    session.close()
    start_end_dt = list(np.ravel(results))
    return jsonify(start_end_dt)

            
if __name__ == "__main__":
    app.run(debug=True)
