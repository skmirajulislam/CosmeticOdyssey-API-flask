
from flasgger import Swagger

def configure_swagger(app):
    app.config['SWAGGER'] = {
        'title': 'Cosmetic Odyssey API',
        'uiversion': 3,
        'description': 'This is the API documentation for this Flask-based backend server.',
        'version': '1.0',
    }
    Swagger(app) 

    return app
