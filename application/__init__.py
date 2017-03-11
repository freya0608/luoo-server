import os

from flask import Flask

from .database import db
from .blueprints.api import api_bp


def format_database_uri(user, password, host, database_name):
    return "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(user, password, host, database_name)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.default")
    app.config.from_object(os.environ.get("FLASK_APP_SETTINGS"))
    app.config.from_pyfile("application.py")
    app.config['SQLALCHEMY_DATABASE_URI'] = format_database_uri(app.config['DATABASE_USER'],
                                                                app.config['DATABASE_PASSWORD'],
                                                                app.config['DATABASE_HOST'],
                                                                app.config['DATABASE_NAME'])
    return app

app = create_app()
app.register_blueprint(api_bp, url_prefix="/api")
db.init_app(app)


from . import views
