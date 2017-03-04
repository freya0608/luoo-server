from flask import Flask

from application.database import db
from application.blueprints.api import api_bp


def format_database_uri(user, password, host, database_name):
    return "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(user, password, host, database_name)


def create_app():
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object("application.config")
    application.config.from_pyfile("application.cfg", silent=True)
    application.config['SQLALCHEMY_DATABASE_URI'] = format_database_uri(application.config['DATABASE_USER'],
                                                                        application.config['DATABASE_PASSWORD'],
                                                                        application.config['DATABASE_HOST'],
                                                                        application.config['DATABASE_NAME'])
    return application

app = create_app()
app.register_blueprint(api_bp, url_prefix="/api")
db.init_app(app)


from . import views
