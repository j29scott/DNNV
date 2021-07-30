#!/bin/bash

set -e

sudo apt update
sudo apt install -y software-properties-common build-essential
sudo apt update
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y cmake wget git liblapack-dev openssl libssl-dev valgrind libtool libboost1.71-all-dev libglpk-dev qt5-qmake libltdl-dev protobuf-compiler

sudo apt install python-is-python3
sudo apt install python3.8-venv
./manage.sh init
. .env.d/openenv.sh
./manage.sh install reluplex planet mipverify neurify eran plnn marabou nnenum verinet

