#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api

# Add your model imports
from models import User, Report, ReportedPhoto, Location, LocationType, LocationFeature, ReportedFeature

# Views go here!
class Index(Resource):
    def get(self):
        return "<h1>Project Server</h1>"

api.add_resource(Index, "/")

class LocationList(Resource): # List all locations
    def get(self):
        locations = [location.to_dict(only=("id", "name", "address", "phone", "location_type_id")) for location in Location.query.all()]
        return locations, 200

api.add_resource(LocationList, "/locations")

class LocationDetail(Resource): # Reports for individual locations
    def get(self, location_id):
        reports = [report.to_dict() for report in Report.query.filter_by(location_id=location_id).all()]
        return reports, 200

    def post(self, location_id):
        try:
            new_report = Report(
                user_id = request.json.get("user_id"),
                location_id = request.json.get("location_id")
            )
            db.session.add(new_report)
            db.session.commit()

            return new_report.to_dict(), 201
        
        except ValueError as e:
            db.session.rollback()
            return {"errors": str(e)}, 400
        except Exception as e:
            return {"errors": str(e)}, 400

    def patch(self, location_id):
        location = Location.query.get(location_id)

        if location is None:
            return {"message": "Location not found"}, 404
        
        

    def delete(self, location_id):
        pass

if __name__ == "__main__":
    app.run(port=5555, debug=True)

