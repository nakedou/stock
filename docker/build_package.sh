#!/bin/bash

if [ ! -d venv ]; then
    virtualenv -p $(which python3.4) venv
fi

source venv/bin/activate

pip_home=$HOME/.pip

pip2 install Mysql-python

pip install -r requirements.txt

npm install --python=python2.7
node_modules/bower/bin/bower install --config.interactive=false --allow-root

invoke -e clean assets.compile pkg.docker