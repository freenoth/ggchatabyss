#!/usr/bin/env bash

source /var/venv/ggchatabyss/bin/activate

pip3 install -r requirements.txt

python3 /var/www/ggchatabyss/manage.py migrate
python3 /var/www/ggchatabyss/manage.py collectstatic --no-input -v 0

python3 /var/www/ggchatabyss/manage.py crontab remove
python3 /var/www/ggchatabyss/manage.py crontab add

deactivate

sudo systemctl restart uwsgi
