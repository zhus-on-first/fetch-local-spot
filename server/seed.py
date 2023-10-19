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

def create_reports():
    reports = []
    for _ in range(10):
        r = Report(
            user = rc(users),
            location = rc(locations)
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
    for _ in range(5):
        loc = Location(
           name = fake.name(),
           address = fake.address(),
           phone = fake.phone_number(),
           location_type_id = randint(1, 3)
        )
        locations.append(loc)

    return locations

def create_location_types():
    location_type_names = ["find a hike", "find a food spot", "find a ride"]
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
        "Other"
    ]

    for location in locations:
        for feature_name in features_list:
            # 50/50
            if rc([True, False]):
                location_feature = LocationFeature(
                    location_id=location.id,
                    feature=feature_name
                    )
            return location_feature

def create_reported_features():
    reported_features = []

    for report in reports:
        # Get all location features for associated report location
        location_features = LocationFeature.query.filter_by(location_id=report.location_id).all()

        # Randomly set how many features report will have
        num_features_in_report = randint(1, 4)

        # Randomly select some of the features
        selected_features = random.sample(location_features, num_features_in_report)

        for feature in selected_features:
            comment = fake.sentence()
            reported_feature = ReportedFeature(
                report_id=report.id, 
                location_feature_id=feature.id, 
                comment=comment
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
        LocationFeature.query.delete()
        ReportedFeature.query.delete()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding reports...")
        reports = create_reports()
        db.session.add_all(reports)
        db.session.commit()

        print("Seeding reported photos...")
        reported_photos = create_reported_photos()
        db.session.add_all(reported_photos)
        db.session.commit()

        print("Seeding locations...")
        locations = create_locations()
        db.session.add_all(locations)
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