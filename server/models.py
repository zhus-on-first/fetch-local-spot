from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # A user has many reports
    reports = db.relationship("Report", back_populates="user", lazy=True)

    # Association Proxy

    # Serialization
    serialize_rules = ("-reports.user")

    def __repr__(self):
        return f"<User(id={self.id}: username={self.username}, email={self.email}, password={self.password})>"

class Report(db.Model, SerializerMixin):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)

    # A report has many reported_features
    reported_features = db.relationship("ReportedFeature", back_populates="report", lazy=True)

    # A report has many reported_photos
    reported_photos = db.relationship("ReportedPhoto", back_populates="report", lazy=True)

    # A report has a/belongs to a user
    user = db.relationship("User", back_populates="reports", lazy=True)

    # A report has a/belongs to a location
    location = db.relationship("Location", back_populates="reports", lazy=True)

    # Has many features through reported_features: report.features
    features = association_proxy("reported_features", "location_features.feature")

    # Has many locations through reported_features: report.locations
    locations = association_proxy("reported_features", "location_features.location")

    # Serialization
    serialize_rules = ("-reported_photos.reports", "-user.reports", "-location.reports")

    def __repr__(self):
        return f"<Report(id={self.id}: user_id={self.user_id}, location_id={self.location_id})>"

class ReportedPhoto(db.Model, SerializerMixin):
    __tablename__ = "reported_photos"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)

    # A reported photo has a/belongs to a report
    report = db.relationship("Report", back_populates="reported_photos", lazy=True)

    # Has many features through reported_features
    features = association_proxy("reported_features", "location_feature.feature")

    # Serialization
    serialize_rules = ("-report.reported_photos",)

    def __repr__(self):
        return f"<ReportPhoto(id={self.id}: report_id={self.report_id}, photo_url={self.photo_url})>"

class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    location_type_id = db.Column(db.Integer, db.ForeignKey('location_types.id'), nullable=False)


    # A location has many location features
    location_features = db.relationship("LocationFeature", back_populates="location", lazy=True)

    # A location has many reports
    reports = db.relationship("Report", back_populates="location", lazy=True)

    # A location has a/belongs to type
    type = db.relationship("LocationType", back_populates="locations", lazy=True)

    # Has many features through location_features: location.features
    features = association_proxy("location_features", "feature")

    # Has many photos through reported_photos
    photo_urls = association_proxy("reported_photos", "photo_url")

    # Serialization
    serialize_rules = ("-type.locations", "-reports.locations", "-location_features.locations")

    def __repr__(self):
        return f"<Location(id={self.id}: name={self.name}, address={self.address}, phone={self.phone}, type_id={self.type_id})>"

class LocationType(db.Model): # one of "find a hike", "find a food spot", or "find a ride"
    __tablename__ = "location_types" 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # A location type has many locations
    locations = db.relationship("Location", back_populates="type", lazy=True)

    # Association Proxy


    # Serialize rule
    serialize_rules = ("-locations.location_types",)

    def __repr__(self):
        return f"<LocationType(id={self.id}: name={self.name})>"

class LocationFeature(db.Model, SerializerMixin):
    __tablename__ = "location_features"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    feature = db.Column(db.String(20), nullable=False)

    # A location feature has a/belongs to a location
    location = db.relationship("Location", back_populates="location_features", lazy=True)

    # A location feature is referenced by many reported_features
    reported_features = db.relationship("ReportedFeature", back_populates="location_feature", lazy=True)

    # Has many reports through reported_features: location_feature.reports --all reports associated with a feature
    reports = association_proxy("reported_features", "report")

    # Serialization
    serialize_rules = ("-location.location_features", "-reported_features.location_features")

    def __repr__(self):
        return f"<LocationFeature(id={self.id} location_id={self.location_id}, feature={self.feature})>"

class ReportedFeature(db.Model, SerializerMixin):
    __tablename__ = "reported_features"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False)
    location_feature_id = db.Column(db.Integer, db.ForeignKey("location_features.id"), nullable=False)

    # A reported_feature has a/belongs to a report
    report = db.relationship("Report", back_populates="reported_features", lazy=True)

    # A reported_feature has a reference to a location feature
    location_feature = db.relationship("LocationFeature", back_populates="reported_features", lazy=True)

    # Association Proxy

    # Serialization
    serialize_rules = ("-location_feature.reported_features")

    def __repr__(self):
        return f"<ReportedFeature(id={self.id} report_id={self.report_id} location_feature_id={self.location_feature_id})>"