# Remote library imports
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate, fields
from faker import Faker

# Local imports
from config import db
from models import Feature, Report, ReportedPhoto, User, Location

fake = Faker()
class UserSchema(SQLAlchemyAutoSchema):

    # Define attributes    
    id = auto_field(dump_only=True)
    username = auto_field(required=False, validate=validate.Length(min=5, error="User name must be at least 5 characters."))
    email = auto_field(required=False, validate=validate.Email())

    # Define Meta class
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

class LocationSchema(SQLAlchemyAutoSchema):

    # Define attributes
    id = auto_field(dump_only=True)
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
      

class FeatureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
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
     
class GetReportSchema(SQLAlchemyAutoSchema):

    # Define attributes
    id = auto_field(dump_only=True)
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
    id = auto_field(dump_only=True)
    user_id = auto_field(required=True)
    location_id = auto_field(required=True, validate=validate.Range(min=1))
    comment = auto_field(allow_none=True)

    # Custom fields to accept incoming reported_features and photo_urls
    reported_features_ids = fields.List(fields.Integer(), required=True)
    photo_urls = fields.List(fields.URL(), required=False)

    # Define Meta class
    class Meta:
        model = Report
        load_instance = False
        sqla_session = db.session
        include_fk = True

class GetReportsByLocationIdSchema(SQLAlchemyAutoSchema):

    # Define attributes
    id = auto_field(dump_only=True)
    user_id = fields.Function(lambda obj: obj.user.id)
    username = fields.Function(lambda obj: obj.user.username)
    user = fields.Nested(UserSimpleSchema)
    location_id = auto_field(required=True)
    comment = auto_field(allow_none=True)
    reported_features_names = fields.Function(lambda obj: [feature.feature_name for feature in obj.reported_features])
    reported_photos = fields.List(fields.Nested(ReportedPhotoSchema))

    # Define Meta class
    class Meta:
        model = Report
        load_instance = True
        sqla_session = db.session

class PatchReportByIdSchema(SQLAlchemyAutoSchema):
    # Update fields
    user_id = fields.Integer(required=True)
    location_id = fields.Integer(required=True)
    comment = fields.String(allow_none=True)

    # Custom fields to accept incoming reported_features and photo_urls
    reported_features = fields.List(fields.Integer(), required=False)
    photos = fields.List(fields.URL(), required=False)

    class Meta:
        model = Report
        load_instance = False
        sqla_session = db.session

patch_report_schema = PatchReportByIdSchema()
