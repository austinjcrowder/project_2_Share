import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/shark.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples = Base.classes.shark_data_cleaned


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])


@app.route("/metadata/<sample>")
def samples(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples.sample,
        Samples.Date,
        Samples.Year,
        Samples.Type,
        Samples.Country,
        Samples.Area,
        Samples.Location,
        Samples.Activity,
        Samples.Name,
        Samples.Sex,
        Samples.Age,
        Samples.Injury
        

    ]

    results = db.session.query(*sel).filter(Samples.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    samples = {}
    for result in results:
        samples["sample"] = result[0]
        samples["ETHNICITY"] = result[1]
        samples["GENDER"] = result[2]
        samples["AGE"] = result[3]
        samples["LOCATION"] = result[4]
        samples["BBTYPE"] = result[5]
        samples["WFREQ"] = result[6]

    print(samples)
    return jsonify(samples)



if __name__ == "__main__":
    app.run()
