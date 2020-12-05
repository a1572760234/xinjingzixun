from flask import Blueprint
from flask_restful import Api
from .views import ImageCodeResource

passport_bp = Blueprint('passport', __name__, url_prefix='/passport')
passport_api = Api(passport_bp)
passport_api.add_resource(ImageCodeResource, 'image_code')
from . import views
