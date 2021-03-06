from flask import Blueprint
from flask_restful import Api

from application.resources import SongResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(SongResource, "/songs/<int:song_id>")

