from flask import request, jsonify
from models import db, Hotel, Package
from flasgger import swag_from

# Add a new hotel
@swag_from({
    'tags': ['Hotel'],
    'description': 'Add a new hotel to the system.',
    'parameters': [
        {
            'name': 'name',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The name of the hotel.'
        },
        {
            'name': 'location',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The location of the hotel.'
        },
        {
            'name': 'amenities',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'Amenities provided by the hotel.'
        },
        {
            'name': 'price_range',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'Price range for services offered by the hotel.'
        },
        {
            'name': 'ratings',
            'in': 'json',
            'type': 'number',
            'required': True,
            'description': 'Ratings for the hotel (1 to 5).'
        }
    ],
    'responses': {
        '201': {
            'description': 'Hotel added successfully.'
        },
        '400': {
            'description': 'Missing required fields or invalid input.'
        },
        '409': {
            'description': 'Hotel with the same name and location already exists.'
        }
    }
})
def add_hotel():
    data = request.get_json()
    required_fields = ['name', 'location',
                       'amenities', 'price_range', 'ratings']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields!"}), 400

    # Check for duplicates (e.g., by name and location)
    existing_hotel = Hotel.query.filter_by(
        name=data['name'], location=data['location']).first()
    if existing_hotel:
        return jsonify({"message": "Hotel with the same name and location already exists!"}), 409

    # Create new hotel
    new_hotel = Hotel(
        name=data['name'],
        location=data['location'],
        amenities=data['amenities'],
        price_range=data['price_range'],
        ratings=data['ratings']
    )

    # Add to database
    db.session.add(new_hotel)
    db.session.commit()
    return jsonify({"message": "Hotel added successfully!"}), 201

# Get all hotels

@swag_from({
    'tags': ['Hotel'],
    'description': 'Retrieve a list of all hotels.',
    'responses': {
        '200': {
            'description': 'List of all hotels.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'hotel_id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'location': {'type': 'string'},
                        'amenities': {'type': 'string'},
                        'price_range': {'type': 'string'},
                        'ratings': {'type': 'number'}
                    }
                }
            }
        },
        '404': {
            'description': 'No hotels found.'
        }
    }
})
def get_all_hotels():
    hotels = Hotel.query.all()
    if not hotels:
        return jsonify({"message": "No hotels found."}), 404

    return jsonify([{
        "hotel_id": hotel.id,
        "name": hotel.name,
        "location": hotel.location,
        "amenities": hotel.amenities,
        "price_range": hotel.price_range,
        "ratings": hotel.ratings
    } for hotel in hotels]), 200

# Get a specific hotel by ID

@swag_from({
    'tags': ['Hotel'],
    'description': 'Retrieve details of a specific hotel by its ID.',
    'parameters': [
        {
            'name': 'hotel_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The hotel ID to retrieve.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Hotel details.',
            'schema': {
                'type': 'object',
                'properties': {
                    'hotel_id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'location': {'type': 'string'},
                    'amenities': {'type': 'string'},
                    'price_range': {'type': 'string'},
                    'ratings': {'type': 'number'}
                }
            }
        },
        '404': {
            'description': 'Hotel not found.'
        }
    }
})

def get_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({"message": "Hotel not found!"}), 404

    return jsonify({
        "hotel_id": hotel.id,
        "name": hotel.name,
        "location": hotel.location,
        "amenities": hotel.amenities,
        "price_range": hotel.price_range,
        "ratings": hotel.ratings
    }), 200

# Update a hotel


@swag_from({
    'tags': ['Hotel'],
    'description': 'Update the details of an existing hotel.',
    'parameters': [
        {
            'name': 'hotel_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The hotel ID to update.'
        },
        {
            'name': 'name',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'The name of the hotel.'
        },
        {
            'name': 'location',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'The location of the hotel.'
        },
        {
            'name': 'amenities',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Amenities provided by the hotel.'
        },
        {
            'name': 'price_range',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Price range for services offered by the hotel.'
        },
        {
            'name': 'ratings',
            'in': 'json',
            'type': 'number',
            'required': False,
            'description': 'Ratings for the hotel (1 to 5).'
        }
    ],
    'responses': {
        '200': {
            'description': 'Hotel details updated successfully.'
        },
        '404': {
            'description': 'Hotel not found.'
        }
    }
})

def update_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({"message": "Hotel not found!"}), 404

    data = request.get_json()
    if 'name' in data:
        hotel.name = data['name']
    if 'location' in data:
        hotel.location = data['location']
    if 'amenities' in data:
        hotel.amenities = data['amenities']
    if 'price_range' in data:
        hotel.price_range = data['price_range']
    if 'ratings' in data:
        hotel.ratings = data['ratings']

    db.session.commit()
    return jsonify({"message": "Hotel details updated successfully!"}), 200

# Delete a hotel


@swag_from({
    'tags': ['Hotel'],
    'description': 'Delete a hotel by its ID.',
    'parameters': [
        {
            'name': 'hotel_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The hotel ID to delete.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Hotel deleted successfully.'
        },
        '404': {
            'description': 'Hotel not found.'
        }
    }
})

def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({"message": "Hotel not found!"}), 404

    db.session.delete(hotel)
    db.session.commit()
    return jsonify({"message": "Hotel deleted successfully!"}), 200
