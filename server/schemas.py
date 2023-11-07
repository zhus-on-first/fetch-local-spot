# Remote library imports
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate, fields, post_load
from faker import Faker

# Local imports
from config import db
from models import Report, ReportedFeature, ReportedPhoto, User, Location

fake = Faker()
class UserSchema(SQLAlchemyAutoSchema):

    # Define attributes    
    id = auto_field()
    username = auto_field(required=True, validate=validate.Length(min=5, error="User name must be at least 5 characters."))
    email = auto_field(required=True, validate=validate.Email())

    # Define Meta class
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True    

class LocationSchema(SQLAlchemyAutoSchema):

    # Define attributes
    id = auto_field()
    name = auto_field(required=True, validate=validate.Length(min=1))
    address = auto_field(required=True, validate=validate.Length(min=1))
    phone = auto_field(allow_none=True, validate=validate.Length(min=15, error="US phone numbers must be at least 15 digits when including area code."))
    reported_features_names = fields.Function(lambda obj: [
        {
            "id": reported_feature.id,
            "reported_feature_name": reported_feature.feature.name
        }
            for report in obj.reports
            for reported_feature in report.reported_features
    ])
    location_type_name = fields.Function(lambda obj: obj.location_type.name if obj.location_type else None)
    location_feature_names = fields.Function(lambda obj: [
        {
            "id": location_feature.id,
            "location_feature_name": location_feature.feature_name
        }
        for location_feature in obj.location_features
    ])

    # Define Meta class
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session    

class UserSimpleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "username")
        load_instance = True
        sqla_session = db.session

class ReportedPhotoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ReportedPhoto
        load_instance = True
        sqla_session = db.session

class ReportedFeatureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ReportedFeature
        load_instance = True
        sqla_session = db.session

class GetReportSchema(SQLAlchemyAutoSchema):

    # Define attributes
    id = auto_field()
    user = fields.Nested(UserSimpleSchema)
    location_id = auto_field(required=True)
    comment = auto_field(allow_none=True)
    reported_feature_names = fields.Function(lambda obj: [feature.feature_name for feature in obj.reported_features])
    reported_photos = fields.List(fields.Nested(ReportedPhotoSchema))

    # Define Meta class
    class Meta:
        model = Report
        load_instance = True
        sqla_session = db.session
class PostReportSchema(SQLAlchemyAutoSchema):

    # Report model fields
    id = auto_field()
    user_id = auto_field(required=True)
    location_id = auto_field(required=True, validate=validate.Length)
    comment = auto_field(allow_none=True)

    # Related objects' fields
    reported_features = fields.List(
        fields.Nested(ReportedFeatureSchema),
        required=True,
        error_messages={"required": "Reported features are required for creating a new report. Please include at least one feature."}
    )
    photo_urls = fields.List(fields.Nested(ReportedPhotoSchema), required=False)

    # Define methods
    @post_load
    def create_report(self, data, **kwargs):
        # Get user data from deserialized data
        user_id = data.get("user_id")

        # Check if user already exists in db
        user = User.query.filter_by(id=user_id).first()

        # If not, create new user with fake values
        if not user:
            user = User(
                id = user_id,
                username = fake.user_name(),
                email =fake.email(),
                password = fake.password()
            )
            db.session.add(user)
            db.session.flush()  # Ensure it gets an ID
        
        # Create the report instance
        new_report = Report(
            user_id=user_id,
            location_id=data.get('location_id'),
            comment=data.get('comment')
        )
        db.session.add(new_report)
        db.session.flush()

        # Handle reported photos
        photo_data = data.get("reported_photos", [])
        photos = [ReportedPhoto(**photo) for photo in photo_data]
        
        
        # db.session.add(new_photo)
        # for photo_url in data.get("photo_urls", []):
        #     new_photo = ReportedPhoto(
        #         report_id=new_report.id,
        #         photo_url=photo_url
        #     )
        #     db.session.add(new_photo)

        # Handle reported features
        feature_data = data.get("reported_features", [])
        features = [ReportedFeature(**feature) for feature in feature_data]

        # Create the report instance
        report = Report(**data)

        # Add photos and features to the report
        report.reported_photos.extend(photos)
        report.reported_features.extend(features)

        return report

    # Define Meta class
    class Meta:
        model = Report
        load_instance = True
        sqla_session = db.session