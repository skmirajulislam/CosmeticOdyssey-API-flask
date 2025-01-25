# Cosmetic Odyssey API

This project provides a Flask-based backend server for managing bookings, users, clinics, hotels, and packages. It comes with Swagger-powered API documentation for easy reference and testing.

---

## Features

- **Booking Management**: Create, update, delete, and fetch bookings.
- **User Management**: Register users, update roles, and fetch user details.
- **Clinic Management**: Add, update, delete, and search clinics.
- **Hotel Management**: Manage hotel-related data.
- **Package Management**: Suggest packages and handle CRUD operations.
- **API Documentation**: Swagger UI for testing API endpoints.

---

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flasgger
- Flask-Swagger-UI

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Update the `Config` class in `config.py` with your database URI.

5. Initialize the database:
   ```bash
   flask shell
   >>> from models import db
   >>> db.create_all()
   >>> exit()
   ```

6. Run the server:
   ```bash
   python app.py
   ```

---

## Endpoints

### Bookings
- **POST** `/bookings`: Create a new booking.
- **PUT** `/bookings/<booking_id>`: Update an existing booking.
- **DELETE** `/bookings/<booking_id>`: Delete a booking.
- **GET** `/bookings`: Retrieve all bookings.
- **GET** `/users/<user_id>/bookings`: Retrieve bookings for a specific user.
- **GET** `/bookings/<booking_id>`: Retrieve details of a specific booking.

### Users
- **POST** `/users`: Register a new user.
- **POST** `/login`: Login a user.
- **DELETE** `/users/<user_id>`: Delete a user.
- **GET** `/users`: Retrieve all users.
- **GET** `/users/<user_id>`: Retrieve user details.
- **PUT** `/users/<user_id>/role`: Update a user's role.

### Clinics
- **POST** `/clinics`: Add a new clinic.
- **PUT** `/clinics/<clinic_id>`: Update clinic details.
- **DELETE** `/clinics/<clinic_id>`: Delete a clinic.
- **GET** `/clinics`: Retrieve all clinics.
- **GET** `/clinics/<clinic_id>`: Retrieve details of a specific clinic.
- **GET** `/clinics/search`: Search clinics.

### Hotels
- **POST** `/hotels`: Add a new hotel.
- **PUT** `/hotels/<hotel_id>`: Update hotel details.
- **DELETE** `/hotels/<hotel_id>`: Delete a hotel.
- **GET** `/hotels`: Retrieve all hotels.
- **GET** `/hotels/<hotel_id>`: Retrieve details of a specific hotel.

### Packages
- **POST** `/packages`: Add a new package.
- **PUT** `/packages/<package_id>`: Update package details.
- **DELETE** `/packages/<package_id>`: Delete a package.
- **GET** `/packages`: Retrieve all packages.
- **GET** `/packages/<package_id>`: Retrieve details of a specific package.
- **POST** `/packages/suggest`: Suggest packages based on user input.

### Root
- **GET** `/api`: Check API root.
- **GET** `/`: Home route.

---

## Swagger API Documentation

The Swagger documentation is available at:
- **UI Version**: `/swagger`
- **JSON Specification**: `/static/swagger.json`

To access Swagger UI:
1. Start the server.
2. Navigate to `http://localhost:8000/swagger` in your browser.

---

## Project Structure

```
.
├── config.py              # Configuration settings
├── models/                # Database models
├── routes/                # All route files (e.g., booking_routes.py)
├── doc/swagger_docs.py    # Swagger documentation configuration
├── router.py              # Route initialization
├── app.py         # Main application file
├── static/                # Static files (including Swagger JSON)
└── requirements.txt       # Python dependencies
```

---

## Contribution

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Support

For support or questions, please contact the maintainer or open an issue in the repository.

