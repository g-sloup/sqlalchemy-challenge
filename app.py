import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>><br/>"
        f"/api/v1.0/<start><end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link from Python to DB
    session = Session(engine)

    # Query for dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").order_by(Measurement.date).all()

    # Convert results to a dictionary using `date` as the key and `prcp` as the value.
    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    session.close()

    # Return the JSON representation of the dictionary
    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create session link from Python to DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset.
    stations = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    # stations_list = list(np.ravel(stations))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create session link from Python to DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station = "USC00519281").
    filter(Measurement.date >= "2016-08-23").all()

    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start(start_date):
    # Create session (link) from Python to DB
    session = Session(engine)
\
    # Query minimum temperature, the average temperature, and the max temperature
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()

    session.close()

    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start_date, end_date):

    # Create session link from Python to DB
    session = Session(engine)

    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)). \
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify(start_end)