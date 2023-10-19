from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from flask import Flask, jsonify


# Set up the Flask app
app = Flask(__name__)

# Database setup (similar to what was shown earlier in the previous response)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create a session for database interactions
session = Session(engine)

# Define the routes

# Route 1: Homepage
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/start_date'>/api/v1.0/start_date</a><br/>"
        f"<a href='/api/v1.0/start_date/end_date'>/api/v1.0/start_date/end_date</a>"
    )

# Route 2: Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in the dataset
    last_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = (dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)).strftime("%Y-%m-%d")
    
    # Query to retrieve the last 12 months of precipitation data
    precipitation_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()
    
    # Convert the result to a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    # Return the JSON representation
    return jsonify(precipitation_dict)

# Route 3: Stations
@app.route("/api/v1.0/stations")
def stations():
    # Query to retrieve a list of stations
    station_list = session.query(station.station, station.name).all()
    
    # Create a list of dictionaries for each station
    station_data = [{"Station": station, "Name": name} for station, name in station_list]
    
    # Return a JSON list of stations
    return jsonify(station_data)

# Route 4: Temperature Observations
@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most active station 
    most_active_station = session.query(measurement.station).group_by(measurement.station).order_by(func.count().desc()).first()[0]
    
    # Calculate the date one year from the last date in the dataset
    last_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = (dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)).strftime("%Y-%m-%d")
    
    # Query to retrieve temperature observations for the most active station in the last 12 months
    tobs_data = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active_station).filter(measurement.date >= one_year_ago).all()
    
    # Create a list of dictionaries for each observation
    tobs_list = [{"Date": date, "Temperature": temp} for date, temp in tobs_data]
    
    # Return a JSON list of temperature observations
    return jsonify(tobs_list)

# Route 5: Temperature Stats for Start Date
@app.route("/api/v1.0/<start_date>")
def temp_stats_start(start_date):
    # Query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to start_date
    temperature_stats = session.query(func.min(measurement.tobs).label("TMIN"),
                                      func.avg(measurement.tobs).label("TAVG"),
                                      func.max(measurement.tobs).label("TMAX"))\
                              .filter(measurement.date >= start_date).all()
    
    # Create a dictionary to store the temperature statistics
    temp_stats_dict = {"Start Date": start_date,
                      "TMIN": temperature_stats[0][0],
                      "TAVG": temperature_stats[0][1],
                      "TMAX": temperature_stats[0][2]}
    
    # Return a JSON representation of the temperature statistics
    return jsonify(temp_stats_dict)

# Route 6: Temperature Stats for Start-End Date Range
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_stats_start_end(start_date, end_date):
    # Query to calculate TMIN, TAVG, and TMAX for dates between start_date and end_date, inclusive
    temperature_stats = session.query(func.min(measurement.tobs).label("TMIN"),
                                      func.avg(measurement.tobs).label("TAVG"),
                                      func.max(measurement.tobs).label("TMAX"))\
                              .filter(measurement.date >= start_date)\
                              .filter(measurement.date <= end_date).all()
    
    # Create a dictionary to store the temperature statistics
    temp_stats_dict = {"Start Date": start_date,
                      "End Date": end_date,
                      "TMIN": temperature_stats[0][0],
                      "TAVG": temperature_stats[0][1],
                      "TMAX": temperature_stats[0][2]}
    
    # Return a JSON representation of the temperature statistics
    return jsonify(temp_stats_dict)

if __name__ == "__main__":
    app.run(debug=True)

# Route 5: Temperature Stats for Start Date
@app.route('/api/v1.0/datesearch/<start_date>')
def temp_stats_start(start_date):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = (session.query(*sel)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)
               .group_by(Measurement.date)
               .all())

    temp_stats = []
    for result in results:
        date_dict = {
            "Date": result[0],
            "TMIN": result[1],
            "TAVG": result[2],
            "TMAX": result[3]
        }
        temp_stats.append(date_dict)

    return jsonify(temp_stats)

# Route 6: Temperature Stats for Start-End Date Range
@app.route('/api/v1.0/datesearch/<start_date>/<end_date>')
def temp_stats_start_end(start_date, end_date):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = (session.query(*sel)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)
               .filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date)
               .group_by(Measurement.date)
               .all())

    temp_stats = []
    for result in results:
        date_dict = {
            "Date": result[0],
            "TMIN": result[1],
            "TAVG": result[2],
            "TMAX": result[3]
        }
        temp_stats.append(date_dict)

    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)
