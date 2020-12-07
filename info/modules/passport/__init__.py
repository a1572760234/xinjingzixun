from flask import Blueprint
from flask_restful import Api
from .views import ImageCodeResource,SMSCodeResource

passport_bp = Blueprint('passport', __name__, url_prefix='/passport')
passport_api = Api(passport_bp)
passport_api.add_resource(ImageCodeResource, '/image_code')
passport_api.add_resource(SMSCodeResource, '/smscode')
from . import views
