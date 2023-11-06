# Standard library imports
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate, fields


# Local imports
from config import db
from models import User, Location

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True
    
    id = auto_field()
    username = auto_field(required=True, validate=validate.Length(min=5))
    email = auto_field(required=True, validate=validate.Email())

class LocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    
    id = auto_field()
    name = auto_field(required=True, validate=validate.Length(min=1))
    address = auto_field(required=True, validate=validate.Length(min=1))
    phone = auto_field(allow_none=True, validate=validate.Length(min=15, error="US phone numbers must be at least 15 digits when including area code."))
    reports = auto_field()
    location_type = auto_field()
    location_type_name = fields.Function(lambda obj: obj.location_type.name if obj.location_type else None)
    location_features = auto_field()
    location_feature_names = fields.Function(lambda obj: [location_feature.feature_name for location_feature in obj.location_features])
