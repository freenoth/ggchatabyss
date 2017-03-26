#!/usr/bin/env bash

rm -rf ~/tmp-ggchatabyss-deploy
rm -rf ~/tmp-ggchatabyss-deploy_backup
mkdir ~/tmp-ggchatabyss-deploy
mkdir ~/tmp-ggchatabyss-deploy_backup

cp -r ggchatabyss/* ~/tmp-ggchatabyss-deploy/
cp -r /var/www/ggchatabyss/ggchatabyss/local_settings.py ~/tmp-ggchatabyss-deploy/ggchatabyss/local_settings.py

cp -r /var/www/ggchatabyss/* ~/tmp-ggchatabyss-deploy_backup/
rm -r /var/www/ggchatabyss/*

cp -r ~/tmp-ggchatabyss-deploy/* /var/www/ggchatabyss/

source /var/venv/ggchatabyss/bin/activate

pip3 install -r requirements.txt
python3 /var/www/ggchatabyss/manage.py migrate
python3 /var/www/ggchatabyss/manage.py collectstatic --no-input -v 0

python3 /var/www/ggchatabyss/manage.py crontab remove
python3 /var/www/ggchatabyss/manage.py crontab add

deactivate

sudo chown -R 1000:www-data /var/www/ggchatabyss

sudo systemctl restart uwsgi

exit 0
