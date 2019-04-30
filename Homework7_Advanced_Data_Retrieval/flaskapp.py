import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set up Flask app
app = Flask(__name__)

#### Flask routes

@app.route("/")
def welcome():
    '''List all available api routes.'''
    return(
    f"Available routes:<br/>"
    f"/api/v1.0///<br>"
    )

    @app.route("/api/v1.0/precipitation")
