# router.py
from routes.booking_routes import add_booking, update_booking, delete_booking, get_all_bookings, get_user_bookings, get_booking
from routes.clinic_routes import add_clinic, update_clinic, delete_clinic, get_all_clinics, get_clinic, search_clinics
from routes.hotel_routes import add_hotel, get_all_hotels, get_hotel, update_hotel, delete_hotel
from routes.package_routes import add_package, update_package, delete_package, get_all_packages, get_package, suggest_packages
from routes.user_routes import register, login, delete_user, get_all_users, get_user, update_user_role
from routes.root_routes import root, home


def add_routes(app):

    # Booking routes
    app.add_url_rule('/bookings', 'add_booking', add_booking, methods=['POST'])
    app.add_url_rule('/bookings/<int:booking_id>',
                     'update_booking', update_booking, methods=['PUT'])
    app.add_url_rule('/bookings/<int:booking_id>',
                     'delete_booking', delete_booking, methods=['DELETE'])
    app.add_url_rule('/bookings', 'get_all_bookings',
                     get_all_bookings, methods=['GET'])
    app.add_url_rule('/users/<int:user_id>/bookings',
                     'get_user_bookings', get_user_bookings, methods=['GET'])
    app.add_url_rule('/bookings/<int:booking_id>',
                     'get_booking', get_booking, methods=['GET'])

    # Clinic routes
    app.add_url_rule('/clinics', 'add_clinic', add_clinic, methods=['POST'])
    app.add_url_rule('/clinics/<int:clinic_id>',
                     'update_clinic', update_clinic, methods=['PUT'])
    app.add_url_rule('/clinics/<int:clinic_id>', 'delete_clinic',
                     delete_clinic, methods=['DELETE'])
    app.add_url_rule('/clinics', 'get_all_clinics',
                     get_all_clinics, methods=['GET'])
    app.add_url_rule('/clinics/<int:clinic_id>', 'get_clinic',
                     get_clinic, methods=['GET'])
    app.add_url_rule('/clinics/search', 'search_clinics',
                     search_clinics, methods=['GET'])

    # Hotel routes
    app.add_url_rule('/hotels', 'add_hotel', add_hotel, methods=['POST'])
    app.add_url_rule('/hotels', 'get_all_hotels',
                     get_all_hotels, methods=['GET'])
    app.add_url_rule('/hotels/<int:hotel_id>', 'get_hotel',
                     get_hotel, methods=['GET'])
    app.add_url_rule('/hotels/<int:hotel_id>', 'update_hotel',
                     update_hotel, methods=['PUT'])
    app.add_url_rule('/hotels/<int:hotel_id>', 'delete_hotel',
                     delete_hotel, methods=['DELETE'])

    # Package routes
    app.add_url_rule('/packages', 'add_package', add_package, methods=['POST'])
    app.add_url_rule('/packages/<int:package_id>',
                     'update_package', update_package, methods=['PUT'])
    app.add_url_rule('/packages/<int:package_id>',
                     'delete_package', delete_package, methods=['DELETE'])
    app.add_url_rule('/packages', 'get_all_packages',
                     get_all_packages, methods=['GET'])
    app.add_url_rule('/packages/<int:package_id>',
                     'get_package', get_package, methods=['GET'])
    app.add_url_rule('/packages/suggest', 'suggest_packages',
                     suggest_packages, methods=['POST'])

    # User routes
    app.add_url_rule('/users', 'register', register, methods=['POST'])
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/users/<int:user_id>', 'delete_user',
                     delete_user, methods=['DELETE'])
    app.add_url_rule('/users', 'get_all_users', get_all_users, methods=['GET'])
    app.add_url_rule('/users/<int:user_id>', 'get_user',
                     get_user, methods=['GET'])
    app.add_url_rule('/users/<int:user_id>/role',
                     'update_user_role', update_user_role, methods=['PUT'])

    # Root
    app.add_url_rule('/api', 'root', root, methods=['GET'])
    app.add_url_rule('/', 'home', home, methods=['GET'])
