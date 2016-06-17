from flask import render_template
from . import main
import tushare as ts


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/users', methods=['GET'])
def users():
    return render_template('user/index.html')


@main.route('/user/<name>', methods=['GET'])
def user(name):
    return render_template('user/_detail.html', name=name)


@main.route('/stocks', methods=['GET'])
def stocks():
    return render_template('stock/index.html')


@main.route('/longhus', methods=['GET'])
def longhus():
    longhus = ts.top_list('2016-06-12')
    return longhus

@main.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')