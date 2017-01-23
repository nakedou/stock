#!/bin/bash

cd $(dirname $0)/..


pip install -r requirements.txt

npm install --python=python2.7
node_modules/bower/bin/bower install

if [ "$(uname -s)" == "Darwin" ] && ! brew list -1 | grep -q pngquant; then
    echo 'Install pngquant on Mac...'
    brew install pngquant
fi
