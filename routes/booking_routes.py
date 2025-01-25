from flask import request, jsonify
from datetime import datetime
from models import db, Booking, User, Clinic, Package
from flasgger import swag_from
# Add a new booking


@swag_from({
    'tags': ['Booking'],
    'description': 'Create a new booking.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'json',
            'type': 'integer',
            'required': True,
            'description': 'The user ID.'
        },
        {
            'name': 'clinic_id',
            'in': 'json',
            'type': 'integer',
            'required': True,
            'description': 'The clinic ID.'
        },
        {
            'name': 'package_id',
            'in': 'json',
            'type': 'integer',
            'required': True,
            'description': 'The package ID.'
        },
        {
            'name': 'appointment_date',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The appointment date in YYYY-MM-DD format.'
        }
    ],
    'responses': {
        '201': {
            'description': 'Booking created successfully.'
        },
        '400': {
            'description': 'Missing required fields or invalid data.'
        },
        '404': {
            'description': 'User, clinic, or package not found.'
        }
    }
})
def add_booking():
    data = request.get_json()
    required_fields = ['user_id', 'clinic_id',
                       'package_id', 'appointment_date']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields!"}), 400

    # Convert appointment_date to datetime object
    try:
        appointment_date = datetime.strptime(
            data['appointment_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Check if the user, clinic, and package exist
    user = User.query.get(data['user_id'])
    clinic = Clinic.query.get(data['clinic_id'])
    package = Package.query.get(data['package_id'])

    if not user or not clinic or not package:
        return jsonify({"message": "Invalid user, clinic, or package!"}), 404

    new_booking = Booking(
        user_id=data['user_id'],
        clinic_id=data['clinic_id'],
        package_id=data['package_id'],
        appointment_date=appointment_date
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Booking made successfully!"}), 201

# Update an existing booking


@swag_from({
    'tags': ['Booking'],
    'description': 'Update an existing booking.',
    'parameters': [
        {
            'name': 'booking_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The booking ID.'
        },
        {
            'name': 'status',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'The new status of the booking.'
        },
        {
            'name': 'appointment_date',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'The new appointment date in YYYY-MM-DD format.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Booking updated successfully.'
        },
        '400': {
            'description': 'Invalid input or date format.'
        },
        '404': {
            'description': 'Booking not found.'
        }
    }
})
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found!"}), 404

    data = request.get_json()
    if not any(key in data for key in ['status', 'appointment_date']):
        return jsonify({"message": "Invalid input! 'status' or 'appointment_date' is required."}), 400

    if 'status' in data:
        booking.status = data['status']

    if 'appointment_date' in data:
        try:
            booking.appointment_date = datetime.strptime(
                data['appointment_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

    db.session.commit()
    return jsonify({"message": "Booking updated successfully!"}), 200

# Delete a booking


@swag_from({
    'tags': ['Booking'],
    'description': 'Delete a booking.',
    'parameters': [
        {
            'name': 'booking_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The booking ID to be deleted.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Booking deleted successfully.'
        },
        '404': {
            'description': 'Booking not found.'
        }
    }
})
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found!"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted successfully!"}), 200

# Get all bookings


@swag_from({
    'tags': ['Booking'],
    'description': 'Retrieve all bookings.',
    'responses': {
        '200': {
            'description': 'List of all bookings.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'booking_id': {'type': 'integer'},
                        'user_id': {'type': 'integer'},
                        'clinic_id': {'type': 'integer'},
                        'package_id': {'type': 'integer'},
                        'status': {'type': 'string'},
                        'appointment_date': {'type': 'string'}
                    }
                }
            }
        },
        '404': {
            'description': 'No bookings found.'
        }
    }
})
def get_all_bookings():
    bookings = Booking.query.all()
    if not bookings:
        return jsonify({"message": "No bookings found."}), 404

    return jsonify([{
        "booking_id": booking.id,
        "user_id": booking.user_id,
        "clinic_id": booking.clinic_id,
        "package_id": booking.package_id,
        "status": booking.status,
        "appointment_date": booking.appointment_date.strftime('%Y-%m-%d')
    } for booking in bookings]), 200

# Get all bookings for a user


@swag_from({
    'tags': ['Booking'],
    'description': 'Retrieve all bookings for a specific user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The user ID.'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of bookings for the user.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'booking_id': {'type': 'integer'},
                        'clinic_id': {'type': 'integer'},
                        'package_id': {'type': 'integer'},
                        'status': {'type': 'string'},
                        'appointment_date': {'type': 'string'}
                    }
                }
            }
        },
        '404': {
            'description': 'No bookings found for this user.'
        }
    }
})
def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
    if not bookings:
        return jsonify({"message": "No bookings found for this user."}), 404

    return jsonify([{
        "booking_id": booking.id,
        "clinic_id": booking.clinic_id,
        "package_id": booking.package_id,
        "status": booking.status,
        "appointment_date": booking.appointment_date.strftime('%Y-%m-%d')
    } for booking in bookings]), 200

# Get a specific booking by ID


@swag_from({
    'tags': ['Booking'],
    'description': 'Retrieve a specific booking by ID.',
    'parameters': [
        {
            'name': 'booking_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The booking ID.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Booking details.',
            'schema': {
                'type': 'object',
                'properties': {
                    'booking_id': {'type': 'integer'},
                    'user_id': {'type': 'integer'},
                    'clinic_id': {'type': 'integer'},
                    'package_id': {'type': 'integer'},
                    'status': {'type': 'string'},
                    'appointment_date': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'Booking not found.'
        }
    }
})
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found!"}), 404

    return jsonify({
        "booking_id": booking.id,
        "user_id": booking.user_id,
        "clinic_id": booking.clinic_id,
        "package_id": booking.package_id,
        "status": booking.status,
        "appointment_date": booking.appointment_date.strftime('%Y-%m-%d')
    }), 200
