from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/stocks', methods=['GET'])
def stocks():
    return render_template('stock/index.html')


@main.route('/book_read', methods=['GET'])
def book_read():
    return render_template('book_read/index.html')


@main.route('/readme', methods=['GET'])
def readme():
    return render_template('user/about_me.html')


@main.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')