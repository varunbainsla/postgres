#!/bin/bash
#Source : https://dev.to/johndotowl/postgresql-16-installation-on-ubuntu-2204-51ia
# Replication setup : https://www.percona.com/blog/setting-up-streaming-replication-postgresql/

sudo apt update
sudo apt install -y gnupg2 wget nano

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

sudo apt update

sudo apt install -y postgresql-16 postgresql-contrib-16

sudo service postgresql start

# Configure PostgreSQL to listen on all interfaces
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/$(ls /etc/postgresql)/main/postgresql.conf

# Allow remote connections to PostgreSQL (replace '0.0.0.0/0' with your actual IP range if needed)
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/$(ls /etc/postgresql)/main/pg_hba.conf

# Restart PostgreSQL service to apply changes
sudo service postgresql restart

# Allow PostgreSQL port through the firewall:
sudo ufw allow 5432/tcp

#Connect as the postgres user:
sudo -u postgres psql

#Set a password for postgres user:
ALTER USER postgres PASSWORD 'postgres123';