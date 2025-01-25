from flask import request, jsonify
from models import db, Package, Clinic
from flasgger import swag_from

# Add a new package


@swag_from({
    'tags': ['Package'],
    'description': 'Add a new package that links a clinic, hotel, and other details.',
    'parameters': [
        {
            'name': 'name',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The name of the package.'
        },
        {
            'name': 'clinic_id',
            'in': 'json',
            'type': 'integer',
            'required': True,
            'description': 'The clinic ID associated with the package.'
        },
        {
            'name': 'hotel_id',
            'in': 'json',
            'type': 'integer',
            'required': True,
            'description': 'The hotel ID associated with the package.'
        },
        {
            'name': 'price',
            'in': 'json',
            'type': 'number',
            'required': True,
            'description': 'Price of the package.'
        },
        {
            'name': 'itinerary',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'Itinerary details of the package.'
        }
    ],
    'responses': {
        '201': {
            'description': 'Package added successfully.'
        },
        '400': {
            'description': 'Missing required fields or invalid input.'
        },
        '409': {
            'description': 'Package with the same name, clinic, and hotel already exists.'
        }
    }
})
def add_package():
    data = request.get_json()
    required_fields = ['name', 'clinic_id', 'hotel_id', 'price', 'itinerary']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields!"}), 400

    # Check for duplicates (e.g., by name, clinic_id, and hotel_id)
    existing_package = Package.query.filter_by(
        name=data['name'], clinic_id=data['clinic_id'], hotel_id=data['hotel_id']).first()
    if existing_package:
        return jsonify({"message": "Package with the same name, clinic, and hotel already exists!"}), 409

    # Create new package
    new_package = Package(
        name=data['name'],
        clinic_id=data['clinic_id'],
        hotel_id=data['hotel_id'],
        price=data['price'],
        itinerary=data['itinerary']
    )

    # Add to database
    db.session.add(new_package)
    db.session.commit()
    return jsonify({"message": "Package added successfully!"}), 201

# Update a package


@swag_from({
    'tags': ['Package'],
    'description': 'Update details of an existing package.',
    'parameters': [
        {
            'name': 'package_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The package ID to update.'
        },
        {
            'name': 'name',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'The name of the package.'
        },
        {
            'name': 'clinic_id',
            'in': 'json',
            'type': 'integer',
            'required': False,
            'description': 'The clinic ID associated with the package.'
        },
        {
            'name': 'hotel_id',
            'in': 'json',
            'type': 'integer',
            'required': False,
            'description': 'The hotel ID associated with the package.'
        },
        {
            'name': 'price',
            'in': 'json',
            'type': 'number',
            'required': False,
            'description': 'Price of the package.'
        },
        {
            'name': 'itinerary',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Itinerary details of the package.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Package details updated successfully.'
        },
        '404': {
            'description': 'Package not found.'
        }
    }
})
def update_package(package_id):
    package = Package.query.get(package_id)
    if not package:
        return jsonify({"message": "Package not found!"}), 404

    data = request.get_json()
    if 'name' in data:
        package.name = data['name']
    if 'clinic_id' in data:
        package.clinic_id = data['clinic_id']
    if 'hotel_id' in data:
        package.hotel_id = data['hotel_id']
    if 'price' in data:
        package.price = data['price']
    if 'itinerary' in data:
        package.itinerary = data['itinerary']

    db.session.commit()
    return jsonify({"message": "Package details updated successfully!"}), 200

# Delete a package


@swag_from({
    'tags': ['Package'],
    'description': 'Delete a package by its ID.',
    'parameters': [
        {
            'name': 'package_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The package ID to delete.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Package deleted successfully.'
        },
        '404': {
            'description': 'Package not found.'
        }
    }
})
def delete_package(package_id):
    package = Package.query.get(package_id)
    if not package:
        return jsonify({"message": "Package not found!"}), 404

    db.session.delete(package)
    db.session.commit()
    return jsonify({"message": "Package deleted successfully!"}), 200

# Get all packages


@swag_from({
    'tags': ['Package'],
    'description': 'Retrieve a list of all available packages.',
    'responses': {
        '200': {
            'description': 'List of all packages.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'package_id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'clinic_id': {'type': 'integer'},
                        'hotel_id': {'type': 'integer'},
                        'price': {'type': 'number'},
                        'itinerary': {'type': 'string'}
                    }
                }
            }
        },
        '404': {
            'description': 'No packages found.'
        }
    }
})
def get_all_packages():
    packages = Package.query.all()
    if not packages:
        return jsonify({"message": "No packages found."}), 404

    return jsonify([{
        "package_id": package.id,
        "name": package.name,
        "clinic_id": package.clinic_id,
        "hotel_id": package.hotel_id,
        "price": package.price,
        "itinerary": package.itinerary
    } for package in packages]), 200

# Get a specific package by ID


@swag_from({
    'tags': ['Package'],
    'description': 'Retrieve details of a specific package by its ID.',
    'parameters': [
        {
            'name': 'package_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The package ID to retrieve.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Package details.',
            'schema': {
                'type': 'object',
                'properties': {
                    'package_id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'clinic_id': {'type': 'integer'},
                    'hotel_id': {'type': 'integer'},
                    'price': {'type': 'number'},
                    'itinerary': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'Package not found.'
        }
    }
})
def get_package(package_id):
    package = Package.query.get(package_id)
    if not package:
        return jsonify({"message": "Package not found!"}), 404

    return jsonify({
        "package_id": package.id,
        "name": package.name,
        "clinic_id": package.clinic_id,
        "hotel_id": package.hotel_id,
        "price": package.price,
        "itinerary": package.itinerary
    }), 200

# Suggest packages based on user preferences


@swag_from({
    'tags': ['Package'],
    'description': 'Suggest packages based on user preferences such as budget, location, or procedure.',
    'parameters': [
        {
            'name': 'budget',
            'in': 'json',
            'type': 'number',
            'required': False,
            'description': 'The maximum budget for the package.'
        },
        {
            'name': 'location',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Preferred location of the clinic.'
        },
        {
            'name': 'procedure',
            'in': 'json',
            'type': 'string',
            'required': False,
            'description': 'Preferred procedure offered by the clinic.'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of suggested packages.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'package_id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'clinic_id': {'type': 'integer'},
                        'hotel_id': {'type': 'integer'},
                        'price': {'type': 'number'},
                        'itinerary': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def suggest_packages():
    preferences = request.get_json()
    query = Package.query
    if 'budget' in preferences:
        query = query.filter(Package.price <= float(preferences['budget']))
    if 'location' in preferences:
        query = query.join(Clinic).filter(
            Clinic.location.contains(preferences['location']))
    if 'procedure' in preferences:
        query = query.join(Clinic).filter(
            Clinic.specialties.contains(preferences['procedure']))
    packages = query.all()
    return jsonify([package.to_dict() for package in packages]), 200
