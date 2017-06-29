from flask import render_template
from flask.blueprints import Blueprint

bp = Blueprint('root', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/stock', methods=['GET'])
def stocks():
    return render_template('stock/index.html')


@bp.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')