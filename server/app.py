#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
from faker import Faker
import logging

# Local imports
from config import app, db, api

# Add your model imports
from models import User, Report, ReportedPhoto, Feature, Location, LocationType, LocationFeature, ReportedFeature

fake = Faker()

# Views go here
class Index(Resource):
    def get(self):
        return "<h1>Project Server</h1>"

api.add_resource(Index, "/")

class UserList(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return users, 200
    
    # def signup(self):
    #     new_user = User(
    #     username = "username", 
    #     email = "email", 
    #     password = hashed
    #     )
    #     return new_user, 200
    
api.add_resource(UserList, "/users")

class LocationList(Resource): # List all locations and useful into
    def get(self):
        locations = [
            {
                **location.to_dict(), 
                "location_type_name": location.location_type_name,
                "location_feature_names": [
                    {
                        "id": location_feature.id,
                        "location_feature_name": location_feature.feature_name
                    }
                    for location_feature in location.location_features],
                "reported_features_names": [
                    {
                        "id": reported_feature.id,
                        "reported_feature_name": reported_feature.feature.name
                    }
                    
                     for report in location.reports for reported_feature in report.reported_features]
            } 
            for location in Location.query.all()
        ]

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
            location_to_dict = {

                **location.to_dict(), 
                "location_type_name": location.location_type_name,
                "location_feature_names": [
                    {
                        "id": location_feature.id,
                        "location_feature_name": location_feature.feature_name
                    }
                    for location_feature in location.location_features],
                "reported_features_names": [
                    {
                        "id": reported_feature.id,
                        "reported_feature_name": reported_feature.feature.name
                    }
                    
                     for report in location.reports for reported_feature in report.reported_features]
            } 
            return location_to_dict, 200
    
api.add_resource(LocationById, "/locations/<int:id>")

class LocationByHikingType(Resource):
    def get(self):
        hiking_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "hike")\
            .all()
        
        hiking_locations_dicts = [
            {
                **location.to_dict(), 
                "location_type_name": location.location_type.name,
                "feature_names": [feature.feature_name for feature in location.location_features]
            } 
            for location in hiking_locations
        ]

        return hiking_locations_dicts, 200
    
api.add_resource(LocationByHikingType, "/locations/find-a-hike")

class LocationByFoodType(Resource):
    def get(self):
        food_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "food")\
            .all()
        
        food_locations_dicts = [
            {
                **location.to_dict(), 
                "location_type_name": location.location_type.name,  
                "feature_names": [feature.feature_name for feature in location.location_features]
            } 
            for location in food_locations
        ]
        return food_locations_dicts, 200
    
api.add_resource(LocationByFoodType, "/locations/find-a-food-spot")

class LocationByRideType(Resource):
    def get(self):
        ride_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "ride")\
            .all()
        
        ride_locations_dicts = [
            {
                **location.to_dict(), 
                "location_type_name": location.location_type.name,
                "feature_names": [feature.feature_name for feature in location.location_features]
            } 
            for location in ride_locations
        ]
        return ride_locations_dicts, 200
    
api.add_resource(LocationByRideType, "/locations/find-a-ride")

class FeatureList(Resource):
    def get(self):
        features = [feature.to_dict() for feature in Feature.query.all()]
        return features, 200
    
api.add_resource(FeatureList, "/features")

class LocationFeaturesByLocationId(Resource):
    def get(self, location_id):
        location_features = [
            {
                **feature.to_dict(), 
                "feature_name": feature.feature_name
            } 
            for feature in LocationFeature.query.filter_by(location_id=location_id).all()
        ]

        return location_features, 200
    
# SAME AS ABOVE
# class LocationFeaturesByLocationId(Resource): 
#     def get(self, location_id):
#         location_features = []
        
#         for feature in LocationFeature.query.filter_by(location_id=location_id).all():
#             feature_dict = feature.to_dict(rules=("feature.name",))
#             feature_dict["feature_name"] = feature.feature_name
#             location_features.append(feature_dict)

#         return location_features, 200
    
api.add_resource(LocationFeaturesByLocationId, "/locations/<int:location_id>/features")

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

logging.basicConfig(level=logging.DEBUG)

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

                # # Remove photos no longer present
                # for photo_url in photos_to_remove:
                #     photo_to_remove = ReportedPhoto.query.filter_by(report_id=report.id, photo_url=photo_url).first()
                #     if photo_to_remove:
                #         logging.debug(f"Found photo to remove: {photo_to_remove}")
                #         db.session.delete(photo_to_remove)
                #     else:
                #         logging.debug(f"Did not find photo to remove for URL: {photo_url}")
                
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

