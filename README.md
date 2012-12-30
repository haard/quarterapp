# Quarterapp




## Usage

Start the server using the command: 

    python quarterapp.py


## Test

Run the unit test using the command

    python test/unit/test.py


## Configuration

Quarterapp uses a Python configuration file that is expected to be located
in the same directory as quarterapp.py (i.e. its working directory) and
be named quarterapp.conf.

An example configuration file is provided under the name quarterapp.example.conf.


### Cookie

Tornado uses a hased cookue value for your secure cookies. Generate and
specify your unique hash.

    cookie_secret = "123"


### MySQL settings

Quarterapp uses the MySQL database and needs the following settings:

    mysql_database = "quarterapp"
    mysql_host = "127.0.0.1:3306"
    mysql_user = "quarterapp"
    mysql_password = "quarterapp"


## Installation


### Install needed tools on Debian

Install tha needed packages for doing python, MySQL and web by running these commands

    sudo apt-get install python-pip python-dev build-essential
    sudo apt-get install mysql-server
    sudo apt-get install libmysqlclient-dev
    sudo pip install --upgrade pip
    sudo pip install tornado
    sudo pip install mysql-python


### Setup the MySQL database.

Login as root by issuing.

    mysql -u root -p

Create the database and a system user.

    create database quarterapp;
    grant all privileges on quarterapp.* to quarterapp@127.0.0.1 identified by 'quarterapp';
    grant all privileges on quarterapp.* to quarterapp@localhost identified by 'quarterapp';

Create the database used for unittesting

    create database quarterapp_test;
    grant all privileges on quarterapp_test.* to quarterapp@127.0.0.1 identified by 'quarterapp';
    grant all privileges on quarterapp_test.* to quarterapp@localhost identified by 'quarterapp';

Run the SQL script to setup the tables needed.

    mysql -u quarterapp -p < quarterapp.sql


### Download quarterapp

TBD


### Configure

Make a copy the example configuration file and enter your specific details. See section #Usage
for details.


## License

Copyright © 2012 Markus Eliasson

Distributed under the BSD License