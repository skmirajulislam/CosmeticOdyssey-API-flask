from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Clinic(db.Model):
    __tablename__ = 'clinic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.JSON, nullable=False)
    specialties = db.Column(db.JSON, nullable=False)
    price_range = db.Column(db.String, nullable=False)
    ratings = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'contact_info': self.contact_info,
            'specialties': self.specialties,
            'price_range': self.price_range,
            'ratings': self.ratings
        }


class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String, nullable=False)
    amenities = db.Column(db.JSON, nullable=False)
    price_range = db.Column(db.String, nullable=False)
    ratings = db.Column(db.Float)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String, default='normal_user')
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey(
        'clinic.id'), nullable=False)  # ForeignKey added
    package_id = db.Column(db.Integer, db.ForeignKey(
        'package.id'), nullable=False)  # ForeignKey added
    status = db.Column(db.String, default='pending')
    appointment_date = db.Column(db.DateTime, nullable=False)


class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey(
        'clinic.id'), nullable=False)  # ForeignKey added
    name = db.Column(db.String(100), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey(
        'hotel.id'), nullable=False)  # ForeignKey added
    price = db.Column(db.Float, nullable=False)
    itinerary = db.Column(db.JSON, nullable=False)
