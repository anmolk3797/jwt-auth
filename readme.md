## Clone the project
Clone the project from Github:

    git clone https://github.com/anmolk3797/jwt-auth.git


## Install Python
    
    sudo apt update && sudo apt install python3.8 virtualenv


# OS Dependencies

    sudo apt update && sudo apt install python3-dev python3.8-dev python3.6-dev build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev



## Database    
Create empty database for the application (e.g. nmbl ):

    sudo -u mysql root

    CREATE DATABASE jwt_auth;


## Settings
Create a copy of .env.example file within settings directory and update your local system configuration in it

    cp jwt-auth/jwt_auth/settings/.env.example jwt-auth/jwt_auth/settings/.env


## Migrate Database

    ./manage.py makemigrations
    
    ./manage.py migrate


## Install Apache Web Server

    sudo apt update && sudo apt install apache2

Enable modules:

    sudo a2enmod rewrite

If We need ssl:

    sudo a2enmod ssl

## Install WSGI Dependencies

    sudo apt update && sudo apt install libapache2-mod-wsgi-py3

    
> **Note:** More information [here](https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/modwsgi/) and [here](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-debian-8)
