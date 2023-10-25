#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc, sample

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Report, ReportedPhoto, Location, LocationType, LocationFeature, ReportedFeature

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
        comment = fake.sentence()
        r = Report(
            user = rc(users),
            location = rc(locations),
            comment=comment
        )
        reports.append(r)

    return reports

def create_reported_photos():
    reported_photos = []

    for report in reports:
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
    
def create_location_features():
    features_list = [
        "Seating with heat lamps",
        "Covered seating",
        "Dogs allowed inside",
        "Reservation system",
    ]

    location_features = []

    for location in locations:

        # Randomly decide if location will have features
        if rc([True, False]):
            num_features = randint(0, 4)
            selected_features = sample(features_list, num_features)
            for feature_name in selected_features:
                    location_feature = LocationFeature(
                        location_id=location.id,
                        feature=feature_name
                        )
                    location_features.append(location_feature)
    return location_features

def create_reported_features():
    reported_features = []

    for report in reports:
        # Get all location features for associated report location
        location_features = LocationFeature.query.filter_by(location_id=report.location_id).all()

        if location_features is not None:
            # Randomly set how many features report will have
            num_features_in_report = randint(0, min(5, len(location_features)))
            print(f"Report ID: {report.id}, Number of Reported Features: {num_features_in_report}, Total Location Features: {len(location_features)}")

            if num_features_in_report > 0:
                # Randomly select some of the features
                selected_features = sample(location_features, num_features_in_report)

                for feature in selected_features:
                    reported_feature = ReportedFeature(
                        report_id=report.id, 
                        location_feature_id=feature.id, 
                        )
                    reported_features.append(reported_feature)
        else:
            pass

    return reported_features
   
if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        Report.query.delete()
        ReportedPhoto.query.delete()
        Location.query.delete()
        LocationType.query.delete()
        LocationFeature.query.delete()
        ReportedFeature.query.delete()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding locations...")
        locations = create_locations()
        db.session.add_all(locations)
        db.session.commit()

        print("Seeding reports...")
        reports = create_reports(users, locations)
        db.session.add_all(reports)
        db.session.commit()

        print("Seeding reported photos...")
        reported_photos = create_reported_photos()
        db.session.add_all(reported_photos)
        db.session.commit()

        print("Seeding location types...")
        location_types = create_location_types()
        db.session.add_all(location_types)
        db.session.commit()

        print("Seeding location features...")
        location_features = create_location_features()
        db.session.add_all(location_features)
        db.session.commit()

        print("Seeding reported features...")
        reported_features = create_reported_features()
        db.session.add_all(reported_features)
        db.session.commit()

        print("Done seeding!")