#!/bin/bash

version="v1.0"

docker build -t fanzheng1101/ddot-anaconda2:$version -f Dockerfile-anaconda2 .
docker tag fanzheng1101/ddot-anaconda2:$version fanzheng1101/ddot-anaconda2:latest

docker build -t fanzheng1101/ddot-anaconda3:$version -f Dockerfile-anaconda3 .
docker tag fanzheng1101/ddot-anaconda3:$version fanzheng1101/ddot-anaconda3:latest

