#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api

# Add your model imports
from models import User, Report, ReportedPhoto, Location, LocationType, LocationFeature, ReportedFeature

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
            return location.to_dict(), 200
    
api.add_resource(LocationById, "/locations/<int:id>")

class LocationByHikingType(Resource):
    def get(self):
        hiking_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "hike")\
            .all()
        
        hiking_locations_dicts = [location.to_dict() for location in hiking_locations]
        return hiking_locations_dicts, 200
    
api.add_resource(LocationByHikingType, "/locations/find-a-hike")

class LocationByFoodType(Resource):
    def get(self):
        food_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "food")\
            .all()
        
        food_locations_dict = [location.to_dict() for location in food_locations]
        return food_locations_dict, 200
    
api.add_resource(LocationByFoodType, "/locations/find-a-food-spot")

class LocationByRideType(Resource):
    def get(self):
        ride_locations = db.session.query(Location)\
            .join(LocationType)\
            .filter(LocationType.name == "ride")\
            .all()
        
        ride_locations_dict = [location.to_dict() for location in ride_locations]
        return ride_locations_dict, 200
    
api.add_resource(LocationByRideType, "/locations/find-a-ride")

class LocationFeaturesByLocationId(Resource):
    def get(self, location_id):
        location_features = [
            feature.to_dict() for feature 
            in LocationFeature.query.filter_by(location_id=location_id).all()
            ]
        
        return location_features, 200
    
api.add_resource(LocationFeaturesByLocationId, "/locations/<int:location_id>/features")
class ReportList(Resource):
    def get(self):
        reports = [report.to_dict() for report in Report.query.all()]
        return reports, 200
    
    def post(self):
        try:
            data = request.json

            new_report = Report(
                user_id = data.get("user_id"),
                location_id = data.get("location_id"),
                comment = data.get("comment")
            )
            db.session.add(new_report)
            db.session.flush()

            for photo_url in data.get("photos", []):
                new_photo = ReportedPhoto(
                    report_id=new_report.id,
                    photo_url=photo_url
                )
                db.session.add(new_photo)

            # Handle Features
            # For each feature, set the LocationFeature. 
            # Match to its corresponding location_feature_id in ReportedFeature
            # Then insert it into the ReportedFeature table, linked to the new report's ID.

            for feature_name in data["features"]:
                # Check if feature already exists for this location
                location_feature = LocationFeature.query.filter_by(
                    location_id=new_report.location_id, feature=feature_name
                    ).first()
                
                # If feature name doesn't exist, create a new entry
                if location_feature is None:
                    location_feature = LocationFeature( # 1. Lookup the corresponding location_feature_id
                        location_id=new_report.location_id, feature=feature_name
                    )
                    db.session.add(location_feature)
                    db.session.flush()

                # Create new ReportFeature entry to link LocationFeature to Report
                report_location_new_feature = ReportedFeature(    
                    report_id=new_report.id,
                    location_feature_id=location_feature.id # 2. Set it in the ReportFeature table
                )
                db.session.add(report_location_new_feature)
                            
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
        report = db.session.query(Report).filter_by(id=id).first()
        if report is None:
            return {"message": "Report not found"}, 404
        else:
            return report.to_dict(), 200
    
    def patch(self, report_id):
        report = db.session.query(Report).filter_by(id=id).first()
        if report is None:
            return {"message": "Report not found"}, 404
        else:
            try:
                for attr in request.json:
                    setattr(report, attr, request.json.get(attr))
                db.session.commit()
                return report.to_dict(), 200
            except Exception as e:
                db.session.rollback()
                return {"errors": str(e)}, 400

    def delete(self, report_id):
        report = db.session.query(Report).filter_by(id=id).first()
        if report is None:           
            return {"message": "Report not found"}, 404
        else:
            db.session.delete(report)
            db.session.commit()
            return {"message": "Report deleted"}, 200
        
# class ReportByLocationId(Resource): # Reports for individual locations
#     def get(self, location_id):
#         reports = [report.to_dict() for report in Report.query.filter_by(location_id=location_id).all()]
#         return reports, 200

#     def patch(self, location_id):
#         report = Report.query.get(location_id)

#         if report is None:
#             return {"message": "Location not found"}, 404
#         else:
#             try:
#                 for attr in request.json:
#                     setattr(report, attr, request.json.get(attr))

#                 db.session.add(report)
#                 db.session.commit()
#                 return report.to_dict("-reported_features", "-reported_photos", "-user", "-location"), 200

#             except ValueError as e:
#                 db.session.rollback()
#                 return {"errors": str(e)}, 400
#             except Exception as e:
#                 return {"errors": str(e)}, 400                
        
#     def delete(self, location_id):
#         report = Report.query.get(location_id)

#         if report is None:
#             return {"message": "Location not found"}, 404
#         else:
#             try:
#                 db.session.delete(report)
#                 db.session.commit()
#                 return {"message": "Report deleted successfully"}, 200
#             except Exception as e:
#                 db.session.rollback()
#                 return {"errors": str(e)}, 400
            
# api.add_resource(ReportByLocationId, "/reports/<int:location_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

