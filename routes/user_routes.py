from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flasgger import swag_from


# User Registration Route
@swag_from({
    'tags': ['User'],
    'description': 'Register a new user.',
    'parameters': [
        {
            'name': 'username',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The username of the user.'
        },
        {
            'name': 'email',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The email of the user.'
        },
        {
            'name': 'password',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The password for the user.'
        }
    ],
    'responses': {
        '201': {
            'description': 'User registered successfully.'
        },
        '400': {
            'description': 'Invalid input or missing fields.'
        },
        '409': {
            'description': 'User already exists with the same email or username.'
        }
    }
})
def register():
    data = request.get_json()
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({"message": "Invalid input! 'username', 'email', and 'password' are required."}), 400

    existing_user = User.query.filter((User.email == data['email']) | (
        User.username == data['username'])).first()
    if existing_user:
        return jsonify({"message": "A user with the same email or username already exists."}), 409

    hashed_password = generate_password_hash(
        data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'],
                    email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# User Login Route


@swag_from({
    'tags': ['User'],
    'description': 'Login an existing user.',
    'parameters': [
        {
            'name': 'email',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The email of the user.'
        },
        {
            'name': 'password',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The password for the user.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Login successful.',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'role': {'type': 'string'}
                }
            }
        },
        '400': {
            'description': 'Invalid input or missing fields.'
        },
        '401': {
            'description': 'Invalid credentials.'
        }
    }
})
def login():
    data = request.get_json()
    if not all(key in data for key in ['email', 'password']):
        return jsonify({"message": "Invalid input! 'email' and 'password' are required."}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful!", "user_id": user.id, "username": user.username, "role": user.role}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

# Delete a user


@swag_from({
    'tags': ['User'],
    'description': 'Delete a user by their ID.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The user ID to be deleted.'
        }
    ],
    'responses': {
        '200': {
            'description': 'User deleted successfully.'
        },
        '404': {
            'description': 'User not found.'
        }
    }
})
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

# Get all users


@swag_from({
    'tags': ['User'],
    'description': 'Retrieve all users.',
    'responses': {
        '200': {
            'description': 'List of all users.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'user_id': {'type': 'integer'},
                        'username': {'type': 'string'},
                        'email': {'type': 'string'},
                        'role': {'type': 'string'}
                    }
                }
            }
        },
        '404': {
            'description': 'No users found.'
        }
    }
})
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users found."}), 404
    return jsonify([{"user_id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users]), 200

# Get a particular user


@swag_from({
    'tags': ['User'],
    'description': 'Retrieve a specific user by ID.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The user ID to retrieve.'
        }
    ],
    'responses': {
        '200': {
            'description': 'User details.',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'role': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'User not found.'
        }
    }
})
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    return jsonify({"user_id": user.id, "username": user.username, "email": user.email, "role": user.role}), 200

# Update a user's role


@swag_from({
    'tags': ['User'],
    'description': 'Update the role of a specific user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The user ID to update.'
        },
        {
            'name': 'role',
            'in': 'json',
            'type': 'string',
            'required': True,
            'description': 'The new role for the user.'
        }
    ],
    'responses': {
        '200': {
            'description': 'User role updated successfully.'
        },
        '404': {
            'description': 'User not found.'
        },
        '400': {
            'description': 'No role specified.'
        }
    }
})
def update_user_role(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    if 'role' in data:
        user.role = data['role']
        db.session.commit()
        return jsonify({"message": "User role updated successfully!"}), 200
    return jsonify({"message": "No role specified!"}), 400
