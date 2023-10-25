#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc, sample

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Report, ReportedPhoto, Feature, Location, LocationType, LocationFeature, ReportedFeature

fake = Faker()

def create_users():
    users = []
    for _ in range(2):
        u = User(
            username = fake.user_name(),
            email = fake.email(),
            password = fake.password()
        )
        users.append(u)

    return users

def create_reports(users, locations):
    reports = []

    for _ in range(10):
        # Create new report
        comment = fake.sentence()
        r = Report(
            user = rc(users),
            location = rc(locations),
            comment=comment
        )
        reports.append(r)

    return reports

def create_reported_photos(reports):
    reported_photos = []

    for report in reports:
            if rc([True, False]):
                img_width = randint(100, 500)
                img_height = randint(100, 500)
                photo_url = f"https://picsum.photos/{img_width}/{img_height}"

                reported_photo = ReportedPhoto(report_id=report.id, photo_url=photo_url)
                reported_photos.append(reported_photo)

    return reported_photos

def create_locations():
    locations = []
    for _ in range(10):
        loc = Location(
           name = fake.name(),
           address = fake.address(),
           phone = fake.phone_number(),
           location_type_id = randint(1, 3)
        )
        locations.append(loc)

    return locations

def create_location_types():
    location_type_names = ["hike", "food", "ride"]
    location_types = []   

    for location_type_name in location_type_names:
        location_type = LocationType(name=location_type_name)
        location_types.append(location_type)
 
    return location_types

def create_features():
    features_list = [
        "Seating with heat lamps",
        "Covered seating",
        "Dogs allowed inside",
        "Reservation system",
    ]
    features = []

    for feature_name in features_list:
        feature=Feature(name=feature_name)
        features.append(feature)

    return features
    
def create_location_features(locations, features):
    location_features = []

    for location in locations:
        # Randomly decide if location will have features
        if rc([True, False]):
            num_features = randint(0, 4)
            selected_features = sample(features, num_features)

            for feature in selected_features:
                location_feature = LocationFeature(
                    location_id=location.id,
                    feature_id=feature.id
                    )
                location_features.append(location_feature)
    return location_features

def create_reported_features(reports, features):
    reported_features = []

    for report in reports:
        # Randomly set how many features report will have
        num_features_in_report = randint(0, min(4, len(features)))

        # Randomly select some of the features
        selected_features = sample(features, num_features_in_report)

        # Get names of selected features
        selected_feature_names = [feature.name for feature in selected_features]

        print(f"Report ID: {report.id}, Number of Reported Features: {num_features_in_report}, Total Features: {len(features)}, Selected Features: {selected_feature_names}")


        for feature in selected_features:
            reported_feature = ReportedFeature(
                report_id=report.id, 
                feature_id=feature.id, 
                )
            reported_features.append(reported_feature)

    return reported_features
   
if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        Report.query.delete()
        ReportedPhoto.query.delete()
        Location.query.delete()
        LocationType.query.delete()
        Feature.query.delete()
        LocationFeature.query.delete()
        ReportedFeature.query.delete()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding locations...")
        locations = create_locations()
        db.session.add_all(locations)
        db.session.flush()

        print("Seeding reports...")
        reports = create_reports(users, locations)
        db.session.add_all(reports)
        db.session.commit()

        print("Seeding reported photos...")
        reported_photos = create_reported_photos(reports)
        db.session.add_all(reported_photos)
        db.session.commit()

        print("Seeding location types...")
        location_types = create_location_types()
        db.session.add_all(location_types)
        db.session.commit()

        print("Seeding features")
        features = create_features()
        db.session.add_all(features)
        db.session.flush()

        print("Seeding location features...")
        location_features = create_location_features(locations, features)
        db.session.add_all(location_features)
        db.session.flush()

        print("Seeding reported features...")
        reported_features = create_reported_features(reports, features)
        db.session.add_all(reported_features)
        db.session.commit()

        print("Done seeding!")