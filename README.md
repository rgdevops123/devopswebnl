[![Build Status](https://travis-ci.com/rgdevops123/devopswebnl.svg?branch=master)](https://travis-ci.com/rgdevops123/devopswebnl)
[![Coverage Status](https://coveralls.io/repos/github/rgdevops123/devopswebnl/badge.svg?branch=master)](https://coveralls.io/github/rgdevops123/devopswebnl?branch=master)

# devopswebnl
### Dev Ops Web with No Login.

### Get the code from GITHUB

    $ git clone https://github.com/rgdevops123/devopswebnl.git
    $ cd devopswebnl


### Install Python 3.6.5

    $ sudo yum -y update
    $ sudo yum -y install yum-utils

    $ sudo yum -y groupinstall development
    $ sudo yum -y install openssl-devel postfix sqlite-devel vim wget zlib-devel
    
    $ wget https://github.com/openssl/openssl/archive/OpenSSL_1_0_2l.tar.gz
    $ tar -zxvf OpenSSL_1_0_2l.tar.gz 
    $ cd openssl-OpenSSL_1_0_2l/
    
    $ ./config shared
    $ make
    $ sudo make install
    $ export LD_LIBRARY_PATH=/usr/local/ssl/lib/
    
    $ cd ..
    $ rm OpenSSL_1_0_2l.tar.gz
    $ rm -rf openssl-OpenSSL_1_0_2l/
    
    $ wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
    $ tar xJf Python-3.6.5.tar.xz
    $ cd Python-3.6.5
    
    $ ./configure
    $ make
    $ sudo make install
    
    $ cd ..
    $ rm Python-3.6.5.tar.xz
    $ sudo rm -rf Python-3.6.5


### Install Requirements

    $ sudo /usr/local/bin/pip3 install -r requirements.txt

 
### ============================================
### Running th Application

### Create a .env.sh file for flask and gunicorn.

    $ vim .env.sh
    export DEVOPSWEB_CONFIG_MODE=Production
    export SECRET_KEY='your-secret-key'
    export SQLALCHEMY_TRACK_MODIFICATIONS=False


### Create a .env file for docker-compose and docker --env-file option.
    $ vim .env
    DEVOPSWEB_CONFIG_MODE=Production
    SECRET_KEY=your-secret-key
    SQLALCHEMY_TRACK_MODIFICATIONS=False


### Source your devopsweb profile for commands "flask" and "gunicorn".

    $ . ./.env.sh


### Set FLASK APP
    $ export FLASK_APP=devopswebnl.py
        OR
    $ export FLASK_APP=./devopswebnl.py
        OR
    $ export FLASK_APP=/FULL_PATH_TO/devopswebnl.py


### Run the Application
       Using gunicorn.
    $ /usr/bin/gunicorn --config gunicorn.py devopswebnl:app &

       Using flask.
    $ flask run --host=0.0.0.0 --port=5000

       Using docker.
    $ sudo docker build . -t rgdevops123/devopswebnl
    $ sudo docker run --env-file .env -d --rm --name devopswebnl -p 5000:5000 rgdevops123/devopswebnl
        --env-file .env     ### Use .env environment file.
        -d                  ### Detached mode: Run the container in the background.
        --rm                ### Automatically remove the container when it exits.
        --name devopswebnl  ### Name the Docker container devopswebnl.
        -p 5000:5000        ### Publish a container's port. hostPort:containerPort


### ============================================
### Run Tests
    $ pytest -v --disable-pytest-warnings
       -v                          ### Verbose
       --disable-pytest-warnings   ### Disable pytest warnings.

    $ pytest -v --disable-pytest-warnings -k unittests
       -v                          ### Verbose
       --disable-pytest-warnings   ### Disable pytest warnings.
       -k <substring>              ### Only run tests with substring.

    $ nose2 -v -s tests_unittests
       -v                          ### Verbose
       -s START_DIR                ### Directory to start discovery ('.' default)

### ============================================
### Run coverage.py
    $ coverage run --source=./app -m pytest -v --disable-pytest-warnings
    $ coverage report
    $ coverage html

