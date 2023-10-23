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

class Signup(Resource):
    def signup(self):
        new_user = User(
        username = "username", 
        email = "email", 
        password = hashed
        )
        return new_user, 200

class Index(Resource):
    def get(self):
        return "<h1>Project Server</h1>"

api.add_resource(Index, "/")

class LocationList(Resource): # List all locations
    def get(self):
        locations = [location.to_dict() for location in Location.query.all()]
        return locations, 200
    
    def post(self):
        print("Received POST request")
        try:
            new_location = Location(
                name = request.json.get("name"),
                address = request.json.get("address"),
                phone = request.json.get("phone"),
                location_type_id= request.json.get("location_type_id")
            )
            db.session.add(new_location)
            db.session.commit()

            # Add handling of location_features, reports, and location_type
            return new_location.to_dict(), 201
        
        except ValueError as e:
            db.session.rollback()
            return {"errors": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"errors": str(e)}, 400 

api.add_resource(LocationList, "/locations")

class LocationById(Resource):
    def get(self, id):
        location = Location.query.filter_by(id=id).first()
        if location is None:
            return {"error": "Location not found"}, 404
        else:
            return location.to_dict(rules=("-location_features", "-reports", "-location_type")), 200
    
api.add_resource(LocationById, "/locations/<int:id>")

class LocationByHikingType(Resource):
    def get(self):
        hiking_locations = [location.to_dict() for location in Location.query.filter_by(location_type_name="hike")]
        return hiking_locations, 200
    
api.add_resource(LocationByHikingType, "/locations/find-a-hike")

class LocationByFoodType(Resource):
    def get(self):
        food_locations = [location.to_dict() for location in Location.query.filter_by(location_type_name="food")]
        return food_locations, 200
    
api.add_resource(LocationByFoodType, "/locations/find-a-food-spot")

class LocationByRideType(Resource):
    def get(self):
        ride_locations = [location.to_dict() for location in Location.query.filter_by(location_type_name="ride")]
        return ride_locations, 200
    
api.add_resource(LocationByRideType, "/locations/find-a-ride")

class ReportList(Resource):
    def get(self):
        reports = [report.to_dict() for report in Report.query.all()]
        return reports, 200
    
    def post(self):
        try:
            new_report = Report(
                user_id = request.json.get("user_id"),
                location_id = request.json.get("location_id")
            )
            db.session.add(new_report)
            db.session.commit()

            # Add handling of reported_features and reported_photos
            return new_report.to_dict("-reported_features", "-reported_photos", "-user", "-location"), 201
        
        except ValueError as e:
            db.session.rollback()
            return {"errors": str(e)}, 400
        except Exception as e:
            return {"errors": str(e)}, 400

api.add_resource(ReportList, "/reports")

class ReportById(Resource): # Reports for individual locations
    def get(self, location_id):
        reports = [report.to_dict() for report in Report.query.filter_by(location_id=location_id).all()]
        return reports, 200

    def patch(self, location_id):
        report = Report.query.get(location_id)

        if report is None:
            return {"message": "Location not found"}, 404
        else:
            try:
                for attr in request.json:
                    setattr(report, attr, request.json.get(attr))

                db.session.add(report)
                db.session.commit()
                return report.to_dict("-reported_features", "-reported_photos", "-user", "-location"), 200

            except ValueError as e:
                db.session.rollback()
                return {"errors": str(e)}, 400
            except Exception as e:
                return {"errors": str(e)}, 400                
        
    def delete(self, location_id):
        report = Report.query.get(location_id)

        if report is None:
            return {"message": "Location not found"}, 404
        else:
            try:
                db.session.delete(report)
                db.session.commit()
                return {"message": "Report deleted successfully"}, 200
            except Exception as e:
                db.session.rollback()
                return {"errors": str(e)}, 400
            
api.add_resource(ReportById, "/reports/<int:location_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

