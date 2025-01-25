from flask import jsonify, render_template


def root():
    """
    Root endpoint that serves a welcome message.
    ---
    responses:
        200:
            description: A welcome message
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: 'Welcome to the flask Server!'
    """
    return jsonify({"message": "Welcome to the flask Server! for more visit /apidocs"}), 200



def home():
    return render_template('home.html')
