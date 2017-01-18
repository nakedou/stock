from flask import render_template
from flask.blueprints import Blueprint

bp = Blueprint('root', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/info', methods=['GET'])
def info():
    return render_template('info/index.html')


@bp.route('/holder', methods=['GET'])
def holder():
    return render_template('holder/index.html')


@bp.route('/timeline', methods=['GET'])
def timeline():
    return render_template('timeline/index.html')


@bp.route('/stock', methods=['GET'])
def stocks():
    return render_template('stock/index.html')


@bp.route('/readme', methods=['GET'])
def readme():
    return render_template('user/about_me.html')


@bp.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')