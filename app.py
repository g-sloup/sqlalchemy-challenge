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
session = Session(engine)

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
        f"/api/v1.0/temperature_start/<date><br/>"
        f"/api/v1.0/temperature_start_end/<date_start>/<date_end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").order_by(
        Measurement.date).all()

    # Convert results to a dictionary using `date` as the key and `prcp` as the value.
    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = prcp
        prcp_list.append(prcp_dict)

    # Return the JSON representation of the dictionary
    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    stations = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(stations))

    return jsonify(stations_lists=stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(
        Measurement.date >= "2016-08-23").all()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(temps)


@app.route("/api/v1.0/temperature_start/<date>")
def temperature_start_date(date):
    # Query stations
    temperature_start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                                              func.max(Measurement.tobs)).filter(Measurement.date >= date).all()

    return jsonify(temperature_start_results)


@app.route("/api/v1.0/temperature_start_end/<date_start>/<date_end>")
def temperature_given_start_end(date_start, date_end):
    # Query stations
    temperature_start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                                    func.max(Measurement.tobs)).filter(Measurement.date >= date_start).\
                                    filter(Measurement.date <= date_end).all()

    return jsonify(temperature_start_end_results)


if __name__ == "__main__":
    app.run(debug=True)
