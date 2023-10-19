#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api

# Add your model imports
from models import db, User, Report, ReportedPhoto, Location, LocationType, LocationFeature, ReportedFeature

# Views go here!
class Index(Resource):
    def get(self):
        return "<h1>Project Server</h1>"

api.add_resource(Index, "/")


if __name__ == '__main__':
    app.run(port=5555, debug=True)

