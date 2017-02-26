from flask import Flask

from application.database import db
from application.blueprints.api import api_bp


def create_app():
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:""@localhost/luoo?charset=utf8"
    return application

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix="/api")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:""@localhost/luoo?charset=utf8"
db.init_app(app)


from . import views
