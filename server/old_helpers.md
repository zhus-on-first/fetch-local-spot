#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api

# Add your model imports
from models import User, Report, ReportedPhoto, Feature, Location, LocationType, LocationFeature, ReportedFeature

# When reported features was linked to reported features. 
# Can also use below if want to update location features table when reported features updates
# or two can diverge over time as users report
class ReportList(Resource):
    def get(self):
        reports = [report.to_dict() for report in Report.query.all()]
        return reports, 200
    
    # For each feature, set the LocationFeature. 
    # Match to its corresponding location_feature_id in ReportedFeature
    # Then insert it into the ReportedFeature table, linked to the new report's ID.

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

            for feature_id in data["reported_features", []]:
                # Check if feature already exists for this location
                location_feature = LocationFeature.query.filter_by(
                    location_id=new_report.location_id, 
                    feature_id=feature_id
                    )\
                    .first()
                
                # If feature name doesn't exist, create a new entry
                if location_feature is None:
                    location_feature = LocationFeature( # 1. Lookup the corresponding location_feature_id
                        location_id=new_report.location_id,
                        feature_id=feature_id
                    )
                    db.session.add(location_feature)
                    db.session.flush() # so new entry gets an ID if needed

                # Create new ReportFeature entry to link LocationFeature (either found or just created) to Report
                reported_feature = ReportedFeature(    
                    report_id=new_report.id,
                    feature_id=location_feature.id # 2. Set it in the ReportFeature table
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


class ReportByLocationId(Resource): # Reports for individual locations
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
            
api.add_resource(ReportByLocationId, "/reports/<int:location_id>")



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


class ReportsByLocation(Resource):
    def get(self, location_id):
        try:
            reports = [
                {
                    **report.to_dict(), 
                    "username": report.user.username if report.user else None, # Some reports have no users due to early Report Post API testing
                    "reported_features_names": [feature.feature_name for feature in report.reported_features],
                    "photos": [
                        {
                            "id": reported_photo.id, 
                            "photo_url": reported_photo.photo_url
                        } 
                        for reported_photo in report.reported_photos
                        ] if report.reported_photos is not None and len(report.reported_photos) > 0 else None
                }
                for report in Report.query.filter_by(location_id=location_id).all()
            ]

            return reports, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
api.add_resource(ReportsByLocation, "/reports/location/<int:location_id>")