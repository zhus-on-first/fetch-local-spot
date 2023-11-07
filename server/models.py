from sqlalchemy.ext.associationproxy import association_proxy


from config import db

# Models go here!
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # A user has many reports
    reports = db.relationship("Report", back_populates="user")

    # A user has many reported photos through reports
    reported_photos = association_proxy("reports", "reported_photos")

    def __repr__(self):
        return f"<User(id={self.id}: username={self.username}, email={self.email}, password={self.password})>"

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    comment = db.Column(db.String(255))

    # A report has many reported_features
    reported_features = db.relationship("ReportedFeature", back_populates="report", cascade="all, delete-orphan")

    # A report has many reported_photos
    reported_photos = db.relationship("ReportedPhoto", back_populates="report", cascade="all, delete-orphan")

    # A report has a/belongs to a user
    user = db.relationship("User", back_populates="reports")

    # A report has a/belongs to a location
    location = db.relationship("Location", back_populates="reports")

    # A report has many reported feature names through reported features
    reported_features_names = association_proxy("reported_features", "feature_name")

    def __repr__(self):
        return f"<Report(id={self.id}: user_id={self.user_id}, location_id={self.location_id})>"

class ReportedPhoto(db.Model):
    __tablename__ = "reported_photos"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)

    # A reported photo has a/belongs to a report
    report = db.relationship("Report", back_populates="reported_photos")

    def __repr__(self):
        return f"<ReportPhoto(id={self.id}: report_id={self.report_id}, photo_url={self.photo_url})>"

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    location_type_id = db.Column(db.Integer, db.ForeignKey('location_types.id'))

    # A location has many reports
    reports = db.relationship("Report", back_populates="location")

    # A location has a/belongs to location_type
    location_type = db.relationship("LocationType", back_populates="locations")

    # A location has many location_features
    location_features = db.relationship("LocationFeature", back_populates="location")

    # A location has a location name through location_types
    location_type_name = association_proxy("location_type", "name")

    # A location has many photos through reports
    location_photos = association_proxy("reports", "reported_photos")

    # A location has many location feature names through LocationFeatures
    location_feature_names = association_proxy("location_features", "feature_name")

    # A location has many reported features names through reports
    reported_features_names = association_proxy("reports", "reported_features_names")

    @classmethod
    def get_hiking_locations(cls):
        return cls.query.join(LocationType).filter(LocationType.name == "hike").all()
    
    @classmethod
    def get_food_locations(cls):
        return cls.query.join(LocationType).filter(LocationType.name == "food").all()
    
    @classmethod
    def get_ride_locations(cls):
        return cls.query.join(LocationType).filter(LocationType.name == "ride").all()

    def __repr__(self):
        return f"<Location(id={self.id}: name={self.name}, address={self.address}, phone={self.phone}, location_type_id={self.location_type_id})>"

class LocationType(db.Model): # one of "find a hike", "find a food spot", or "find a ride"
    __tablename__ = "location_types" 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # A location_type has many locations
    locations = db.relationship("Location", back_populates="location_type")

    def __repr__(self):
        return f"<LocationType(id={self.id}: name={self.name})>"

class Feature(db.Model):
    __tablename__ = "features"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    # A feature is referenced by many location_features
    location_features = db.relationship("LocationFeature", back_populates="feature")

    # A feature is referenced by many reported_features
    reported_features = db.relationship("ReportedFeature", back_populates="feature")

class LocationFeature(db.Model):
    __tablename__ = "location_features"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey("features.id"), nullable=False)

    # A location_feature has a/belongs to a location
    location = db.relationship("Location", back_populates="location_features")

    # A location_feature references a feature
    feature = db.relationship("Feature", back_populates="location_features")

    # A location_feature has a name through feature
    feature_name = association_proxy("feature", "name")

    def __repr__(self):
        return f"<LocationFeature(id={self.id} location_id={self.location_id}, feature={self.feature_id})>"

class ReportedFeature(db.Model):
    __tablename__ = "reported_features"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey("features.id"), nullable=False)

    # A reported_feature has a/belongs to a report
    report = db.relationship("Report", back_populates="reported_features")

    # A reported_feature references a feature
    feature = db.relationship("Feature", back_populates="reported_features")

    # A Reported_Feature has a name through Feature
    feature_name = association_proxy("feature", "name")

    def __repr__(self):
        return f"<ReportedFeature(id={self.id} report_id={self.report_id} feature_id={self.feature_id})>"