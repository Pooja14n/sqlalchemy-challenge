# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

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
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

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
            f"/api/v1.0/<start> (enter as YYYY-MM-DD) <br>"
            f"/api/v1.0/<start>/<end> (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )
    
    
# # 2. "/api/v1.0/precipitation"
# @app.route("/api/v1.0/precipitation")
# def precipitation():
    
#     session = Session(engine)
#     results = session.query(measurement.date, measurement.prcp).all()

#     prcp_results = []

#     for date, prcp in results:
#         prcp_dict = {}
#         prcp_dict[date] = prcp
#         prcp_results.append(prcp_dict) 

#     session.close()
#     return jsonify(prcp_results)

# # 3. "/api/v1.0/stations"
# @app.route("/api/v1.0/stations")
# def stations():
    
#     session = Session(engine)    
#     results = session.query(station.id, station.station, station.name, station.latitude, station.longitude, station.elevation).all()
#     session.close()
#     station_list = []
#     for id, station, name, latitude, longitude, elevation in results:
#         station_dict = {}
#         station_dict['Id'] = id
#         station_dict['station'] = station
#         station_dict['name'] = name
#         station_dict['latitude'] = latitude
#         station_dict['longitude'] = longitude
#         station_dict['elevation'] = elevation
#         station_list.append(station_dict)
#     return jsonify(station_list)


# # 4. "/api/v1.0/tobs"
# @app.route("/api/v1.0/tobs")
# def tobs():
#     session = Session(engine) 
#     active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]
    
#     last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
#     # format_str = '%Y-%m-%d'
#     last_dt = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
#     one_year_date = last_dt - dt.timedelta(days=365)

#     active_tobs = session.query(measurement.date, measurement.tobs).filter((measurement.station == active_stations) & (measurement.date >= one_year_date) & (measurement.date <= last_dt)).all()

#     session.close()
#     return jsonify(active_tobs)


# # 5(a) "/api/v1.0/<start>"  
# @app.route("/api/v1.0/<start>")
# def start_date(start):
    
#     session = Session(engine)

#     start_dt = session.query(func.min(measurement.date)).first()[0]
#     end_dt = session.query(func.max(measurement.date)).first()[0]

#     if start >= start_dt and start <= end_dt:
#         temperature = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_dt).filter(measurement.date <= end_dt).all()[0]
    
#         return (
#             f"Min temp: {temperature[0]}</br>"
#             f"Avg temp: {temperature[1]}</br>"
#             f"Max temp: {temperature[2]}"
#             )
    
#     # else:
#     #     return jsonify({"error": f"The date {start} was not found. Please select a date between 2010-01-01 and 2017-08-23."}), 404
    
    

# # 5(b) "/api/v1.0/<start>/<end>"  
# @app.route("/api/v1.0/<start>/<end>")
# def start_end_date(start, end):
   
#     session = Session(engine)

#     start_dt = session.query(func.min(measurement.date)).first()[0]
#     end_dt = session.query(func.max(measurement.date)).first()[0]

#     if start >= start_dt and end <= end_dt:
#         temperature = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()[0]
    
#         return (
#             f"Min temp: {temperature[0]}</br>"
#             f"Avg temp: {temperature[1]}</br>"
#             f"Max temp: {temperature[2]}"
#             )
    
#     # else:
#     #     return jsonify({"error": f"The dates {start} or {end} were not found. Please select dates between 2010-01-01 and 2017-08-23."}), 404
            
            
# if __name__ == "__main__":
#     app.run(debug=True)
