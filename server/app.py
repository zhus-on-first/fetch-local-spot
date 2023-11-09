#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask import request, abort
from flask_restful import Resource
from faker import Faker
import traceback
from svix import Webhook
from svix.exceptions import WebhookVerificationError

# Local imports
from config import app, db, api, auth, svix_api_secret
from services import make_report, patch_report, create_user, delete_user

# Add your model imports
from models import User, Report, Location, Feature
from schemas import FeatureSchema, UserSchema, LocationSchema
from schemas import GetReportSchema, PostReportSchema, GetReportsByLocationIdSchema, patch_report_schema

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

api.add_resource(UserList, "/users")

class SvixWebhookHandler(Resource):
    def post(self):
        # Retrieve the raw payload
        payload = request.get_data(as_text=True)
        
        # Retrieve all headers from the request
        headers = dict(request.headers)

        # Initialize a webhook verification object with your secret
        verifier = Webhook(svix_api_secret)

        try:
            # Verify the signature using the raw payload and all headers
            verifier.verify(payload, headers)
        except WebhookVerificationError:
            abort(401, 'Invalid signature.')

        # If the signature is verified, parse the JSON payload
        payload_json = request.get_json()

        # Access the 'event_type' directly based on your sample payload
        event_type = payload_json['event_type']

        if event_type == "user.created":
            # Access the user information directly
            email = payload_json['email']
            user_id = payload_json['user_id']
            first_name = payload_json.get('first_name')
            last_name = payload_json.get('last_name')
            username = payload_json.get('username')
            picture_url = payload_json.get('picture_url')
            create_user(email, user_id, picture_url, username, first_name, last_name)

        elif event_type == "user.deleted":
            # Access the user ID directly
            user_id = payload_json['user_id']
            delete_user(user_id)

        # Respond to Svix to acknowledge receipt of the webhook
        return {'status': 'success'}, 200

api.add_resource(SvixWebhookHandler, "/svix_user_webhook_endpoint")
class LocationList(Resource):

    @auth.optional_user
    def get(self):
        locations = Location.query.all()
        location_schema = LocationSchema(many=True)

        return location_schema.dump(locations), 200
    
    @auth.require_user
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

    @auth.optional_user
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

    @auth.optional_user
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

    @auth.optional_user
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

    @auth.optional_user
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

    @auth.optional_user
    def get(self):
        features = Feature.query.all()
        feature_schema = FeatureSchema(many=True)
        return feature_schema.dump(features), 200
    
api.add_resource(FeatureList, "/features")
class ReportList(Resource):

    @auth.optional_user
    def get(self):
        reports = Report.query.all()
        report_schema = GetReportSchema(many=True)
        return report_schema.dump(reports), 200
    
    @auth.require_user
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

    @auth.optional_user
    def get(self, report_id):
        report = db.session.query(Report).get(report_id)
        report_schema = GetReportSchema()
        if report:
            return report_schema.dump(report), 200
        else:
            return {"message": "Report not found"}, 404
    
    @auth.require_user
    def patch(self, report_id):
        # Get JSON data from request
        patch_data = request.get_json()

        # Deserialize and validate the request data
        try:
            validated_patch_data= patch_report_schema.load(patch_data)
        except ValidationError as e:
            return {"errors": e.messages}, 400

        try:
            # Call service layer to update the report
            updated_report = patch_report(report_id, validated_patch_data)
            
            # Serialize and return the updated report
            return patch_report_schema.dump(updated_report), 200
        
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {"errors": str(e)}, 400

    @auth.require_user
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

    @auth.optional_user
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

