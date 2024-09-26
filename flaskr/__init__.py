import os
from flask import Flask

def create_app(test_config=None):
    # Creates the Flask app instance with default configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DEBUG = False,
        RDB_HOST = 'localhost',
        RDB_PORT = '28015',
        SECRET_KEY = '8463'
    )
    if test_config is None:
        # Unless testing, load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # If testing load the test config
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Blueprint for functions that manage the database connection
    from . import db
    db.init_app_database(app)

    # Blueprint for routes related to the todos
    from . import todos
    app.register_blueprint(todos.todos_bp)

    # Blueprints for routes related to user authentication
    from . import auth
    app.register_blueprint(auth.auth_bp)

    return app