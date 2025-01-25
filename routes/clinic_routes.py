from flask import request, jsonify
from models import db, Clinic
from flasgger import swag_from

# Add a new clinic


@swag_from({
    'tags': ['Clinic'],
    'description': 'Add a new clinic to the system.',
    'parameters': [
        {
            'name': 'name',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The name of the clinic.'
        },
        {
            'name': 'location',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The location of the clinic.'
        },
        {
            'name': 'contact_info',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'Contact information of the clinic.'
        },
        {
            'name': 'specialties',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'Specialties provided by the clinic.'
        },
        {
            'name': 'price_range',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'Price range for services offered by the clinic.'
        },
        {
            'name': 'ratings',
            'in': 'json',
            'type': 'number',
            'required': True,
            'description': 'Ratings for the clinic (1 to 5).'
        }
    ],
    'responses': {
        '201': {
            'description': 'Clinic added successfully.'
        },
        '400': {
            'description': 'Missing required fields or invalid input.'
        },
        '409': {
            'description': 'Clinic with the same name and location already exists.'
        }
    }
})
def add_clinic():
    data = request.get_json()
    required_fields = ['name', 'location', 'contact_info',
                       'specialties', 'price_range', 'ratings']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields!"}), 400

    # Check for duplicates (e.g., by name and location)
    existing_clinic = Clinic.query.filter_by(
        name=data['name'], location=data['location']).first()
    if existing_clinic:
        return jsonify({"message": "Clinic with the same name and location already exists!"}), 409

    # Create new clinic
    new_clinic = Clinic(
        name=data['name'],
        location=data['location'],
        contact_info=data['contact_info'],
        specialties=data['specialties'],
        price_range=data['price_range'],
        ratings=data['ratings']
    )

    # Add to database
    db.session.add(new_clinic)
    db.session.commit()
    return jsonify({"message": "Clinic added successfully!"}), 201

# Update a clinic's details


@swag_from({
    'tags': ['Clinic'],
    'description': 'Update the details of an existing clinic.',
    'parameters': [
        {
            'name': 'clinic_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The clinic ID to update.'
        },
        {
            'name': 'name',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'The name of the clinic.'
        },
        {
            'name': 'location',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'The location of the clinic.'
        },
        {
            'name': 'contact_info',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Contact information of the clinic.'
        },
        {
            'name': 'specialties',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Specialties provided by the clinic.'
        },
        {
            'name': 'price_range',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Price range for services offered by the clinic.'
        },
        {
            'name': 'ratings',
            'in': 'json',
            'type': 'number',
            'required': False,
            'description': 'Ratings for the clinic (1 to 5).'
        }
    ],
    'responses': {
        '200': {
            'description': 'Clinic details updated successfully.'
        },
        '404': {
            'description': 'Clinic not found.'
        }
    }
})
def update_clinic(clinic_id):
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return jsonify({"message": "Clinic not found!"}), 404

    data = request.get_json()
    if 'name' in data:
        clinic.name = data['name']
    if 'location' in data:
        clinic.location = data['location']
    if 'contact_info' in data:
        clinic.contact_info = data['contact_info']
    if 'specialties' in data:
        clinic.specialties = data['specialties']
    if 'price_range' in data:
        clinic.price_range = data['price_range']
    if 'ratings' in data:
        clinic.ratings = data['ratings']

    db.session.commit()
    return jsonify({"message": "Clinic details updated successfully!"}), 200

# Delete a clinic


@swag_from({
    'tags': ['Clinic'],
    'description': 'Delete a clinic by its ID.',
    'parameters': [
        {
            'name': 'clinic_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The clinic ID to delete.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Clinic deleted successfully.'
        },
        '404': {
            'description': 'Clinic not found.'
        }
    }
})
def delete_clinic(clinic_id):
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return jsonify({"message": "Clinic not found!"}), 404

    db.session.delete(clinic)
    db.session.commit()
    return jsonify({"message": "Clinic deleted successfully!"}), 200

# Get all clinics


@swag_from({
    'tags': ['Clinic'],
    'description': 'Retrieve a list of all clinics.',
    'responses': {
        '200': {
            'description': 'List of all clinics.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'clinic_id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'location': {'type': 'string'},
                        'contact_info': {'type': 'string'},
                        'specialties': {'type': 'string'},
                        'price_range': {'type': 'string'},
                        'ratings': {'type': 'number'}
                    }
                }
            }
        },
        '404': {
            'description': 'No clinics found.'
        }
    }
})
def get_all_clinics():
    clinics = Clinic.query.all()
    if not clinics:
        return jsonify({"message": "No clinics found."}), 404

    return jsonify([{
        "clinic_id": clinic.id,
        "name": clinic.name,
        "location": clinic.location,
        "contact_info": clinic.contact_info,
        "specialties": clinic.specialties,
        "price_range": clinic.price_range,
        "ratings": clinic.ratings
    } for clinic in clinics]), 200

# Get a specific clinic by ID


@swag_from({
    'tags': ['Clinic'],
    'description': 'Retrieve details of a specific clinic by its ID.',
    'parameters': [
        {
            'name': 'clinic_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The clinic ID to retrieve.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Clinic details.',
            'schema': {
                'type': 'object',
                'properties': {
                    'clinic_id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'location': {'type': 'string'},
                    'contact_info': {'type': 'string'},
                    'specialties': {'type': 'string'},
                    'price_range': {'type': 'string'},
                    'ratings': {'type': 'number'}
                }
            }
        },
        '404': {
            'description': 'Clinic not found.'
        }
    }
})
def get_clinic(clinic_id):
    clinic = Clinic.query.get(clinic_id)
    if not clinic:
        return jsonify({"message": "Clinic not found!"}), 404

    return jsonify({
        "clinic_id": clinic.id,
        "name": clinic.name,
        "location": clinic.location,
        "contact_info": clinic.contact_info,
        "specialties": clinic.specialties,
        "price_range": clinic.price_range,
        "ratings": clinic.ratings
    }), 200

# Search clinics by specialties, price range, location, or ratings


@swag_from({
    'tags': ['Clinic'],
    'description': 'Search for clinics based on specialties, price range, location, or ratings.',
    'parameters': [
        {
            'name': 'specialties',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Specialties to filter clinics by.'
        },
        {
            'name': 'price_range',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Price range to filter clinics by.'
        },
        {
            'name': 'location',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Location to filter clinics by.'
        },
        {
            'name': 'ratings',
            'in': 'query',
            'type': 'number',
            'required': False,
            'description': 'Ratings to filter clinics by.'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of clinics matching search criteria.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'clinic_id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'location': {'type': 'string'},
                        'contact_info': {'type': 'string'},
                        'specialties': {'type': 'string'},
                        'price_range': {'type': 'string'},
                        'ratings': {'type': 'number'}
                    }
                }
            }
        }
    }
})
def search_clinics():
    params = request.args
    query = Clinic.query

    if 'specialties' in params:
        query = query.filter(
            Clinic.specialties.contains(params['specialties']))
    if 'price_range' in params:
        query = query.filter_by(price_range=params['price_range'])
    if 'location' in params:
        query = query.filter(Clinic.location.contains(params['location']))
    if 'ratings' in params:
        query = query.filter(Clinic.ratings >= float(params['ratings']))

    clinics = query.all()
    return jsonify([clinic.to_dict() for clinic in clinics]), 200
