#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DB_NAME='evedb'

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi

# Include the "parse_yaml" function
. ${DIR}/parse_yaml.sh

apt-get update

# Install python packages
#apt-get build-dep -y python3-matplotlib
apt-get install -y python3-pip
pip3 install git+git://github.com/pycrest/PyCrest.git
#pip3 install matplotlib
pip3 install sqlalchemy pyaml pymysql

# Install MariaDB (debian jessie)
apt-get install -y software-properties-common
apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
add-apt-repository 'deb [arch=amd64,i386] http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.1/debian jessie main'
apt-get update
apt-get install -y mariadb-server
# Generate/get our keys
python3 ${DIR}/../evelib/Keys.py
eval $(parse_yaml ${DIR}/../.keys.yaml "key_")
if [ -z "$key_sql_user" ]; then
    echo "Error: unable to get sql_user key"
    exit 1
fi
if [ -z "$key_sql_remote_user" ]; then
    echo "Error: unable to get the sql_remote_user key"
    exit 1
fi
# Initalize our db
echo "Enter your MariaDB root password: "
read -s PASSWORD
mysql -u root -p"${PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME"
mysql -u root -p"${PASSWORD}" -e "CREATE USER IF NOT EXISTS 'sql_user'@'localhost' IDENTIFIED BY '${key_sql_user}';"
mysql -u root -p"${PASSWORD}" -e "GRANT CREATE, INSERT, SELECT ON ${DB_NAME}.* TO 'sql_user'@'localhost' IDENTIFIED BY '${key_sql_user}';"
mysql -u root -p"${PASSWORD}" -e "CREATE USER IF NOT EXISTS 'sql_remote_user'@'localhost' IDENTIFIED BY '${key_sql_remote_user}';"
mysql -u root -p"${PASSWORD}" -e "GRANT SELECT ON ${DB_NAME}.* TO 'sql_user'@'%' IDENTIFIED BY '${key_sql_remote_user}';"


