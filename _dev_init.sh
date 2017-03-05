#!/usr/bin/env bash

sudo adduser vagrant www-data

sudo rm -r /var/venv
sudo mkdir /var/venv
sudo chmod 770 /var/venv
sudo chown 1000:www-data /var/venv

pip3 install virtualenv
virtualenv /var/venv/ggchatabyss

sudo mkdir -p /etc/uwsgi/sites
sudo cp -f -r configs/uwsgi/ggchatabyss.ini /etc/uwsgi/sites/

sudo cp -f -r configs/uwsgi/uwsgi.service /etc/systemd/system/

sudo rm /etc/nginx/sites-enabled/*
sudo rm /etc/nginx/sites-available/*
sudo rm /var/www/*

sudo cp -f -r configs/nginx/ggchatabyss.conf /etc/nginx/sites-available/
sudo ln -s -f /etc/nginx/sites-available/ggchatabyss.conf /etc/nginx/sites-enabled

sudo systemctl enable nginx
sudo systemctl enable uwsgi
sudo systemctl enable postgresql

sudo systemctl restart uwsgi
sudo systemctl restart nginx
sudo systemctl restart postgresql
