# Remote library imports
from faker import Faker

# Standard library imports

# Local imports
from config import db
from models import User, Report, ReportedPhoto, ReportedFeature

fake = Faker()

def create_user(email, user_id, picture_url, username, first_name, last_name):
    new_user = User(
        email=email,
        propelauth_user_id=user_id,
        propelauth_picture_url=picture_url,
        propelauth_first_name=first_name,
        propelauth_last_name=last_name,
        propelauth_username=username
    )
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def delete_user(user_id):
    user = User.query.filter_by(propelauth_user_id=user_id).first()
    if user:
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def make_report(new_report_data):
    # Fetch or create the User
    user_id = new_report_data["user_id"]
    user = User.query.filter_by(id=user_id).first()
    if not user:
        # Create a new user using fake data
        user = User(
            id=user_id,
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        db.session.add(user)
        db.session.flush()
    
    # Create the Report instance
    new_report = Report(
        user_id=user.id,
        location_id=new_report_data["location_id"],
        comment=new_report_data.get("comment", None)
    )
    
    db.session.add(new_report)
    db.session.flush()

    # Prepare the reported photos
    for photo_url in new_report_data.get("photo_urls", []):
        new_photos = ReportedPhoto(
            report_id=new_report.id,
            photo_url=photo_url
        )
        db.session.add(new_photos)

    # Prepare the reported features
    for feature_id in new_report_data["reported_features_ids"]:
        new_reported_features = ReportedFeature(    
            report_id=new_report.id,
            feature_id=feature_id
        )
        db.session.add(new_reported_features)
        
    db.session.commit()
    db.session.refresh(new_report)
    new_report.user = user

    return new_report

def patch_report(report_id, patch_data):

    # Find the report to update
    report_to_update = db.session.query(Report).filter_by(id=report_id).first()
    
    # Update the report with the validated data
    for key, value in patch_data.items():
        if key not in ["reported_features", "photos"]:
            setattr(report_to_update, key, value)

    # Handle updating reported features
    # Fetch existing reported features for this report
    # existing_feature_ids = {reported_feature.feature_id for reported_feature in report_to_update.reported_features}
    existing_reported_features = ReportedFeature.query.filter(ReportedFeature.report_id == report_to_update.id).all()
    existing_feature_ids = {reported_feature.feature_id for reported_feature in existing_reported_features}

    # New feature IDs from the request
    new_feature_ids = set(patch_data.get("reported_features", []))

    # Identify features to be added or removed
    features_to_add = new_feature_ids - existing_feature_ids
    features_to_remove = existing_feature_ids - new_feature_ids

    # Add new features
    for feature_id in features_to_add:
        new_feature = ReportedFeature(report_id=report_to_update.id, feature_id=feature_id)
        db.session.add(new_feature)

    # Remove features no longer present
    for feature_id in features_to_remove:
        feature_to_remove = ReportedFeature.query.filter_by(report_id=report_to_update.id, feature_id=feature_id).first()
        if feature_to_remove:
            db.session.delete(feature_to_remove)

    # Handle photos
    # Fetch existing reported photos for this report
    existing_photo_urls = {photo.photo_url for photo in report_to_update.reported_photos}

    # New photo URLs from the request
    # new_photo_urls = set(patch_data.json.get("photos", []))
    new_photo_urls = set(patch_data.get("photos", []))

    # Identify photos to be added or removed
    photos_to_add = new_photo_urls - existing_photo_urls
    photos_to_remove = existing_photo_urls - new_photo_urls

    # Add new photos
    for photo_url in photos_to_add:
        new_photo = ReportedPhoto(report_id=report_to_update.id, photo_url=photo_url)
        db.session.add(new_photo)

    # Remove photos no longer present
    for photo_url in photos_to_remove:
        photo_to_remove = ReportedPhoto.query.filter_by(report_id=report_to_update.id, photo_url=photo_url).first()
        if photo_to_remove:
            db.session.delete(photo_to_remove)
            db.session.flush()

    db.session.commit()

    return report_to_update
