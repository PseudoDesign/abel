#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi

apt-get update

# Install python packages
#apt-get build-dep -y python3-matplotlib
apt-get install -y python3-pip
pip3 install git+git://github.com/pycrest/PyCrest.git
#pip3 install matplotlib
pip3 install sqlalchemy pyaml

# Install MariaDB (debian jessie)
apt-get install -y software-properties-common
apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
add-apt-repository 'deb [arch=amd64,i386] http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.1/debian jessie main'
apt-get update
apt-get install -y mariadb-server
# Generate our keys
python3 ${DIR}/../evelib/Keys.py
