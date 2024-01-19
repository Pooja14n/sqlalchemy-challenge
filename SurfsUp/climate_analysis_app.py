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

    session.close()
    precipitation = list(np.ravel(results))
    return jsonify(precipitation)

# 3. "/api/v1.0/stations"
@app.route("/api/v1.0/stations")
def stations():
              
    results1 = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
  
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

    session.close()
    start_dt = list(np.ravel(results))
    return jsonify(start_dt)


# 5(b) "/api/v1.0/<start>/<end>"  
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
   
    
    starting_date = dt.datetime.strptime(start,'%Y-%m-%d').date()
    ending_date = dt.datetime.strptime(end,'%Y-%m-%d').date()
    
    results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= starting_date).filter(measurement.date <= ending_date).group_by(measurement.date).all()

    session.close()
    start_end_dt = list(np.ravel(results))
    return jsonify(start_end_dt)

            
if __name__ == "__main__":
    app.run(debug=True)
