#!/bin/bash

# обновляем индексы
echo -e "\e[32mUpdate apt-get indexes\e[0m"
sudo apt-get -y update

# устанавливаем обновления
echo -e "\e[32mUpgrade packages\e[0m"
sudo apt-get -y upgrade

# устанавливаем поддержку ssl для питона
echo -e "\e[32mInstall libssl-dev\e[0m"
sudo apt-get install --force-yes libssl-dev libssl-doc zlib1g-dev

# настраиваем директорию
echo -e "\e[32mConfiguring temp directory\e[0m"
cd ~
mkdir temp

# устанавливаем zlib
echo -e "\e[32mInstalling Zlib\e[0m"
cd ~/temp
wget http://zlib.net/zlib-1.2.11.tar.xz --quiet
tar -xf zlib-1.2.11.tar.xz
cd zlib-1.2.11
./configure
sudo make --quiet && sudo make install --quiet

# устанавливаем python 3.6
echo -e "\e[32mInstalling Python3.6\e[0m"
cd ~/temp
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz --quiet
tar -xf Python-3.6.0.tar.xz
cd Python-3.6.0
./configure
sudo make --quiet && sudo make install --quiet

# устанавливаем пакеты для питона
echo -e "\e[32mInstalling Python3.6 packages\e[0m"
pip3 install -U pip
pip3 install virtualenv


echo -e "\e[32mInstalling nginx\e[0m"
sudo apt-get install fontconfig-config fonts-dejavu-core libfontconfig1 libgd3 libvpx1 libxpm4 libxslt1.1 nginx nginx-common nginx-full

echo -e "\e[32mInstalling uwsgi\e[0m"
sudo pip3 install uwsgi

echo -e "\e[32mInstalling PostgreSQL\e[0m"
sudo apt-get install libpq5 postgresql postgresql-9.4 postgresql-client-9.4 postgresql-client-common postgresql-common ssl-cert

echo -e "\e[32mConfiguring PostgreSQL\e[0m"
sudo -u postgres createuser -s admin
sudo -u postgres createdb -O admin ggchatabyss
sudo -u postgres psql -c "alter role admin with password 'password';"


echo -e "\e[32mRunning _DEV_INIT.SH\e[0m"
bash _dev_init.sh

echo -e "\e[32mRunning _DEV_DEPLOY.SH\e[0m"
bash _dev_deploy.sh

echo -e "\e[32mComplete!\e[0m"
exit 0