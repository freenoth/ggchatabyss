#!/usr/bin/env bash

sudo rm -r /var/www/ggchatabyss

sudo cp -f -r ggchatabyss /var/www
sudo chown -R 1000:www-data /var/www/ggchatabyss

sudo rm -r /var/www/ggchatabyss/media/*
sudo rm -r /var/www/ggchatabyss/static/*

source /var/venv/ggchatabyss/bin/activate

pip3 install -r requirements.txt

python3 /var/www/ggchatabyss/manage.py makemigrations
python3 /var/www/ggchatabyss/manage.py migrate

python3 /var/www/ggchatabyss/manage.py collectstatic --no-input

deactivate

sudo systemctl restart uwsgi
