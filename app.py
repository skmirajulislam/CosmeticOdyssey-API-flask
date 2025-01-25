# final_route.py
from flask import Flask
from config import Config
from models import db
from doc.swagger_docs import configure_swagger
from router import add_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    configure_swagger(app)

    with app.app_context():
        # Create all tables in the single database
        db.create_all()
        print("Created tables in the database")

        if db.engine.dialect.name == 'sqlite':
            with db.engine.connect() as connection:
                connection.connection.execute('PRAGMA foreign_keys = ON')

    add_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8000)
