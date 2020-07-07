from flask import Blueprint

home_blueprint = Blueprint('home_blueprint', __name__)

from . import views
