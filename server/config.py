# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from propelauth_flask import init_auth
from dotenv import load_dotenv
import os

# Local imports

# Instantiate app, set attributes

# Load environment variables from .env file
load_dotenv()

# Use environment variables for the PropelAuth configuration
auth_url = os.getenv('PROPELAUTH_URL')
api_key = os.getenv('PROPELAUTH_API_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
auth = init_auth(auth_url, api_key)

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)


# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)