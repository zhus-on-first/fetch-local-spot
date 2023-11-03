# Standard library imports
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate


# Local imports
from config import db
from models import User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True
    
    id = auto_field()
    username = auto_field(validate=validate.Length(min=5))
    email = auto_field(validate=validate.Email())