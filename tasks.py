import os.path

from invoke import Collection

from app import create_app
from task import db as database, misc, pkg, assets
from task.db import get_project_root

_project_root = get_project_root(__file__)

_app = create_app(os.getenv('FLASK_CONFIG') or 'default')

ns = Collection.from_module(misc)
ns.configure({'config': _app.config, 'project_root': _project_root})

ns.add_collection(Collection.from_module(database))
ns.add_collection(Collection.from_module(pkg))
ns.add_collection(Collection.from_module(assets))
