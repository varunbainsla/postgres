***
# EC2 POSTGRES SETUP - MANUAL
***

## Requirement 
* 3 Ubuntu Machine  v22.04
  * Master
  * RSAZ (Read replica in same AZ)
  * RDAZ (Read replica in different AZ)
* Postgres v16

## Setup

Install Postgres 16.v 

source : https://dev.to/johndotowl/postgresql-16-installation-on-ubuntu-2204-51ia

 * ### Step 1 - Add PostgreSQL Repository 

First, update the package index and install required packages:
```commandline
sudo apt update
sudo apt install gnupg2 wget nano
```

Add the PostgreSQL 16 repository:
```commandline
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

Import the repository signing key:
```commandline
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
```

Update the package list:
```commandline
sudo apt update
```

* ### Step 2 - Install PostgreSQL 16

Install PostgreSQL 16 and contrib modules:
```commandline
sudo apt install postgresql-16 postgresql-contrib-16
```

Start and enable PostgreSQL service:
```commandline
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 3 - Configure PostgreSQL 16

* #### Configure PostgreSQL to listen on all interfaces
```
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/$(ls /etc/postgresql)/main/postgresql.conf 
```

* ####  Allow remote connections to PostgreSQL (replace '0.0.0.0/0' with your actual IP range if needed)
```
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/$(ls /etc/postgresql)/main/pg_hba.conf
```

* ####  Restart PostgreSQL service to apply changes
```
sudo service postgresql restart
```

* ####  Allow PostgreSQL port through the firewall:
```
sudo ufw allow 5432/tcp
```

* ####  Connect as the postgres user: 
```
sudo -u postgres psql

#Set a password for postgres user:
ALTER USER postgres PASSWORD 'postgres123';
```




