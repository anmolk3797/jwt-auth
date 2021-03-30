
## Clone the project
Clone the project from Github:

    git clone h## Clone the project
Clone the project from Github:

    git clone https://github.com/omar-codes/pet-hotel-python-anmolk3797.git


## Install Python
    
    sudo apt update && sudo apt install python3.8 virtualenv


# OS Dependencies

    sudo apt update && sudo apt install python3-dev python3.8-dev python3.6-dev build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev


## Install MogoDB

    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
    
    sudo add-apt-repository 'deb [arch=amd64] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse'

    
    sudo apt update && sudo apt install -y mongodb && sudo apt install mongodb-org



## Settings
Create a copy of .env.example file within settings directory and update your local system configuration in it

    cp pet_hotel_backend/pet_hotel/settings/.env.example pet_hotel_backend/pet_hotel/settings/.env


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



## Install Python
    
    sudo apt update && sudo apt install python3.8 virtualenv


# OS Dependencies

    sudo apt update && sudo apt install python3-dev python3.8-dev python3.6-dev build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev


## Install MogoDB

    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
    
    sudo add-apt-repository 'deb [arch=amd64] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse'

    
    sudo apt update && sudo apt install -y mongodb && sudo apt install mongodb-org


## Settings
Create a copy of .env.example file within settings directory and update your local system configuration in it

    cp pet_hotel_backend/pet_hotel/settings/.env.example pet_hotel_backend/pet_hotel/settings/.env


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
