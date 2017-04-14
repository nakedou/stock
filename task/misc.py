import os

from invoke import ctask


@ctask
def server(ctx):
    from app import create_app
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run(debug=True)
