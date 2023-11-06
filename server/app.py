#!/usr/bin/env python3

# Standard library imports
import logging

# Remote library imports
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from faker import Faker

# Local imports
from config import app, db, api

# Add your model imports
from models import User, Report, ReportedPhoto, Feature, Location, LocationType, LocationFeature, ReportedFeature
from schemas import UserSchema, LocationSchema

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
        if location is None:
            return {"error": "Location not found"}, 404
        else:
            location_schema = LocationSchema()
            location_data = location_schema.dump(location)
            return location_data, 200
    
api.add_resource(LocationById, "/locations/<int:id>")

class LocationByHikingType(Resource):
    def get(self):
        hiking_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "hike")\
            .all()
    
        location_schema = LocationSchema(many=True)
        hiking_locations_data = location_schema.dump(hiking_locations)
        return hiking_locations_data, 200
    
api.add_resource(LocationByHikingType, "/locations/find-a-hike")

class LocationByFoodType(Resource):
    def get(self):
        food_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "food")\
            .all()
        
        location_schema = LocationSchema(many=True)
        food_locations_data = location_schema.dump(food_locations)
        return food_locations_data, 200
    
api.add_resource(LocationByFoodType, "/locations/find-a-food-spot")

class LocationByRideType(Resource):
    def get(self):
        ride_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "ride")\
            .all()
        
        location_schema = LocationSchema(many=True)
        ride_locations_data = location_schema.dump(ride_locations)
        return ride_locations_data, 200
    
api.add_resource(LocationByRideType, "/locations/find-a-ride")

class ReportList(Resource):
    def get(self):
        reports = [report.to_dict() for report in Report.query.all()]
        return reports, 200
    
    def post(self):
        try:
            data = request.json
            print(f"Incoming new report data: {data}")

            # Create new user if it doesn't exist
            user_id = data.get("user_id")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                user = User(
                    id = user_id,
                    username = fake.user_name(),
                    email = fake.email(),
                    password = fake.password()
                    )
                db.session.add(user)
                db.session.flush()

            new_report = Report(
                user_id = data.get("user_id"),
                location_id = data.get("location_id"),
                comment = data.get("comment")
            )
            print(f"New Report before adding to session: {new_report}")
            db.session.add(new_report)
            db.session.flush() # To ensure it gets an ID fore photo to reference
            print(f"New Report after flush: {new_report}")

            for photo_url in data.get("photo_urls", []):
                new_photo = ReportedPhoto(
                    report_id=new_report.id,
                    photo_url=photo_url
                )
                db.session.add(new_photo)

            # Handle Features
            for feature_id in data.get("reported_features", []):
                reported_feature = ReportedFeature(    
                    report_id=new_report.id,
                    feature_id=feature_id
                )
                db.session.add(reported_feature)
                            
            db.session.commit()
            return new_report.to_dict(), 201
        
        except ValueError as e:
            db.session.rollback()
            return {"errors": str(e)}, 400
        except Exception as e:
            return {"errors": str(e)}, 400

api.add_resource(ReportList, "/reports")

class ReportById(Resource):
    def get(self, report_id):
        report = db.session.query(Report).filter_by(id=report_id).first()
        if report is None:
            return {"message": "Report not found"}, 404
        else:
            return report.to_dict(), 200
    
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
        try:
            print(f"Querying reports for location_id = {location_id}")

            query_result = Report.query.filter_by(location_id=location_id).all()
            print(f"Query Result: {query_result}")

            reports = [
                {
                    **report.to_dict(), 
                    "username": report.user.username if report.user else None,

                    "reported_features_names": [feature.feature_name for feature in report.reported_features],


                    "photos": [
                        {
                            "id": reported_photo.id, 
                            "photo_url": reported_photo.photo_url
                        } 
                        for reported_photo in report.reported_photos
                    ] if report.reported_photos is not None and len(report.reported_photos) > 0 else None
                }
                for report in query_result
            ]
            print(f"Reports: {reports}")

            return reports, 200
        except Exception as e:
            return {"error": str(e)}, 400

api.add_resource(ReportsByLocationId, "/reports/location/<int:location_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

