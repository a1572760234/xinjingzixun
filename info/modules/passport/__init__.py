from flask import Blueprint


passport_bp = Blueprint('passport',__name__,url_prefix='/passport')
from . import views