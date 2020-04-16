import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temperature/<start><br/>"
        f"/api/v1.0/temperature/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Perform a query to retrieve the data and precipitation scores for last 12 months
    Convert the query results to a dictionary using date as the key and prcp as the value."""
    # last 12 months of precipiation data
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()

    #Convert results to a dictionary using date as the key and prcp as the value
    prcp_data = []
    for date, precipitation in results:
        precip_dict = {}
        precip_dict[date] = precipitation
        prcp_data.append(precip_dict)
  
    session.close()

    
    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data. 
    #Return a JSON list of temperature observations (TOBS) for the previous year.

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.station == "USC00519281").all()

    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year

    return jsonify(results)

@app.route("/api/v1.0/temperature/<start><br/>")
def start_date():

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).group_by(Measurement.date).all()

    return jsonify(results)

    


    
    
if __name__ == '__main__':
    app.run(debug=True)
