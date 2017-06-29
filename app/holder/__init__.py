from flask.blueprints import Blueprint

bp = Blueprint('holder', __name__, template_folder='templates')

from . import views
