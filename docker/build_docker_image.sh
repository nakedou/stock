#!/bin/bash
docker stop stock
docker rm stock
#docker images | grep registry.cn-hangzhou.aliyuncs.com/nakedou/base-4-python | awk '{print $3}' | xargs docker rmi

set -e

build_container_id=`docker run --name 'stock' -w /opt/stock -d registry.cn-hangzhou.aliyuncs.com/nakedou/base-4-python:v7 sleep infinity`

docker cp ./app/ ${build_container_id}:/opt/stock
docker cp ./assets/ ${build_container_id}:/opt/stock
docker cp ./scripts/ ${build_container_id}:/opt/stock
docker cp ./task/ ${build_container_id}:/opt/stock
docker cp ./bower.json ${build_container_id}:/opt/stock
docker cp ./package.json ${build_container_id}:/opt/stock
docker cp ./gulpfile.js ${build_container_id}:/opt/stock
docker cp ./asset-util.js ${build_container_id}:/opt/stock
docker cp ./browserify-shim.js ${build_container_id}:/opt/stock
docker cp ./requirements.txt ${build_container_id}:/opt/stock
docker cp ./run_with_tornado.py ${build_container_id}:/opt/stock
docker cp ./tasks.py ${build_container_id}:/opt/stock
docker cp ./config.py ${build_container_id}:/opt/stock
docker cp ./ngx-runtime ${build_container_id}:/opt/stock
docker cp ./docker/build_package.sh ${build_container_id}:/opt/stock
docker exec ${build_container_id} /opt/stock/build_package.sh
rm -rf ./docker/app
docker cp ${build_container_id}:/opt/stock/docker/app ./docker

docker build docker -t registry.cn-hangzhou.aliyuncs.com/nakedou/stock:latest
docker stop ${build_container_id}
docker rm ${build_container_id}
