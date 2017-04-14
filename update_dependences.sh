#!/bin/bash

pip install -r requirements.txt

npm install --python=python2.7
node_modules/bower/bin/bower install --allow-root

if [ "$(uname -s)" == "Darwin" ] && ! brew list -1 | grep -q pngquant; then
    echo 'Install pngquant on Mac...'
    brew install pngquant
fi
