from flask.blueprints import Blueprint

bp = Blueprint("api", __name__)


from . import info, hodlers
