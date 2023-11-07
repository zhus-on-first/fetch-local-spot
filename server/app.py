#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from faker import Faker
import traceback

# Local imports
from config import app, db, api
from services import make_report

# Add your model imports
from models import User, Report, ReportedPhoto, Location, ReportedFeature, Feature
from schemas import FeatureSchema, UserSchema, LocationSchema, GetReportSchema, PostReportSchema, GetReportsByLocationIdSchema

fake = Faker()

# Views go here
class Index(Resource):
    def get(self):
        return "<h1>Project Server</h1>"

api.add_resource(Index, "/")

class UserList(Resource):
    def get(self):
        users = User.query.all()
        user_schema = UserSchema(many=True)
        return user_schema.dump(users), 200
    
    def post(self):
        user_schema = UserSchema()
        try:
            user_data = request.get_json()
            new_user = user_schema.load(user_data)
            db.session.add(new_user)
            db.session.commit()
            return user_schema.dump(new_user), 201
        except ValidationError as e:
            return e.messages, 400
        except IntegrityError:
            db.session.rollback()
            return {"message": "Username or email already exists."}, 400

api.add_resource(UserList, "/users")

class LocationList(Resource):
    def get(self):
        locations = Location.query.all()
        location_schema = LocationSchema(many=True)

        return location_schema.dump(locations), 200

    def post(self):
        # Initialize schema
        location_schema = LocationSchema()
        # Parse and validate incoming JSON data
        try:
            location_data = request.get_json()  # Get data from request
            new_location = location_schema.load(location_data)  # Deserialize data to new Location object
            db.session.add(new_location)  # Add new Location to session
            db.session.commit()  # Commit session
            return location_schema.dump(new_location), 201  # Serialize and return new Location
        except ValidationError as e:
            db.session.rollback()  # Rollback session if validation errors
            return e.messages, 400
        except IntegrityError:
            db.session.rollback()
            return {"message": "Location with given details already exists."}, 400  

api.add_resource(LocationList, "/locations")

class LocationById(Resource):
    def get(self, id):
        location = Location.query.filter_by(id=id).first()
        if location:
            location_schema = LocationSchema()
            location_data = location_schema.dump(location)
            return location_data, 200
        else:
             return {"error": "Location not found"}, 404

api.add_resource(LocationById, "/locations/<int:id>")

class LocationByHikingType(Resource):
    def get(self):
        try:
            hiking_locations = Location.get_hiking_locations()
            if not hiking_locations:
                return {"message": "No hiking locations found"}, 404
            
            location_schema = LocationSchema(many=True)
            hiking_locations_data = location_schema.dump(hiking_locations)
            return hiking_locations_data, 200
        except Exception as e:
            return {"message": str(e)}, 500
    
api.add_resource(LocationByHikingType, "/locations/find-a-hike")

class LocationByFoodType(Resource):
    def get(self):
        try:
            food_locations = Location.get_food_locations()
            if not food_locations:
                return {"message": "No food locations found"}, 404
            
            location_schema = LocationSchema(many=True)
            food_locations_data = location_schema.dump(food_locations)
            return food_locations_data, 200
        except Exception as e:
            return {"message": str(e)}, 500
    
api.add_resource(LocationByFoodType, "/locations/find-a-food-spot")

class LocationByRideType(Resource):
    def get(self):
        try:
            ride_locations = Location.get_ride_locations()
            if not ride_locations:
                return {"message": "No ride locations found"}, 404
        
            location_schema = LocationSchema(many=True)
            ride_locations_data = location_schema.dump(ride_locations)
            return ride_locations_data, 200
        except Exception as e:
            return {"message": str(e)}, 500
    
api.add_resource(LocationByRideType, "/locations/find-a-ride")

class FeatureList(Resource):
    def get(self):
        features = Feature.query.all()
        feature_schema = FeatureSchema(many=True)
        return feature_schema.dump(features), 200
    
api.add_resource(FeatureList, "/features")
class ReportList(Resource):
    def get(self):
        reports = Report.query.all()
        report_schema = GetReportSchema(many=True)
        return report_schema.dump(reports), 200
     
    def post(self):
        try:
            # Get JSON data from request
            new_report_data = request.json

            # Initialize schema
            report_schema = PostReportSchema()

            # Deserialize JSON data
            deserialized_new_report_data = report_schema.load(new_report_data)

            # Create Report instance with processed data using the service function
            new_report = make_report(deserialized_new_report_data)
            print(new_report.reported_features)
            print(new_report.reported_photos)

            # Return serialized Report
            return report_schema.dump(new_report), 201
        
        except ValidationError as e:
            db.session.rollback()
            return {"Validation errors": e.messages}, 400
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            return {"Exception errors": str(e)}, 400

api.add_resource(ReportList, "/reports")

class ReportById(Resource):
    def get(self, report_id):
        report = db.session.query(Report).get(report_id)
        report_schema = GetReportSchema()
        if report:
            return report_schema.dump(report), 200
        else:
            return {"message": "Report not found"}, 404
    
    def patch(self, report_id):
        report = db.session.query(Report).filter_by(id=report_id).first()
        if report is None:
            return {"message": "Report not found"}, 404
        else:
            try:
                for attr in request.json.keys(): # explicitly pull out keys from json object
                    if attr not in ["reported_features", "photos"]: # check if not one of these
                        setattr(report, attr, request.json.get(attr)) # if not, go ahead and update Report 

                # Handle updating reported features
                # Fetch existing reported features for this report
                existing_feature_ids = {reported_feature.feature_id for reported_feature in report.reported_features}

                # New feature IDs from the request
                new_feature_ids = set(request.json.get("reported_features", []))

                # Identify features to be added or removed
                features_to_add = new_feature_ids - existing_feature_ids
                features_to_remove = existing_feature_ids - new_feature_ids

                # Add new features
                for feature_id in features_to_add:
                    new_feature = ReportedFeature(report_id=report.id, feature_id=feature_id)
                    db.session.add(new_feature)

                # Remove features no longer present
                for feature_id in features_to_remove:
                    feature_to_remove = ReportedFeature.query.filter_by(report_id=report.id, feature_id=feature_id).first()
                    if feature_to_remove:
                        db.session.delete(feature_to_remove)

                # Handle photos

                # Fetch existing reported photos for this report
                existing_photo_urls = {photo.photo_url for photo in report.reported_photos}

                # New photo URLs from the request
                new_photo_urls = set(request.json.get("photos", []))

                # Identify photos to be added or removed
                photos_to_add = new_photo_urls - existing_photo_urls
                photos_to_remove = existing_photo_urls - new_photo_urls

                # Add new photos
                for photo_url in photos_to_add:
                    new_photo = ReportedPhoto(report_id=report.id, photo_url=photo_url)
                    db.session.add(new_photo)

                app.logger.debug(f"About to remove these photos: {photos_to_remove}")
                # Remove photos no longer present
                for photo_url in photos_to_remove:
                    photo_to_remove = ReportedPhoto.query.filter_by(report_id=report.id, photo_url=photo_url).first()
                    if photo_to_remove:
                        db.session.delete(photo_to_remove)
                        db.session.flush()
                
                app.logger.debug("Finished removing photos.")

                db.session.commit()
                return report.to_dict(), 200
                
            except Exception as e:
                db.session.rollback()
                return {"errors": str(e)}, 400

    def delete(self, report_id):
        report = db.session.query(Report).filter_by(id=report_id).first()
        if report is None:           
            return {"message": "Report not found"}, 404
        else:
            db.session.delete(report)
            db.session.commit()
            return {"message": "Report deleted"}, 200

api.add_resource(ReportById, "/reports/<int:report_id>")

class ReportsByLocationId(Resource):
    def get(self, location_id):
        reports = Report.query.filter_by(location_id=location_id).all()
        reports_schema = GetReportsByLocationIdSchema(many=True)
        if reports:
            return reports_schema.dump(reports), 200
        else:
            return {"error": "No reports found for this location"}, 404

api.add_resource(ReportsByLocationId, "/reports/location/<int:location_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

