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

## создаём виртуальную среду для приложения
#echo -e "\e[32mMaking virtual environment\e[0m"
#cd /vagrant/source
#rm -r venv
#
#virtualenv -p python3.6 --always-copy venv
#
## activate virtual env
#source venv/bin/activate

pip3 install asyncio

pip3 install django

pip3 install djangorestframework
pip3 install markdown       # Markdown support for the browsable API.
pip3 install django-filter  # Filtering support

pip3 install requests

pip3 install websockets

pip3 install aiohttp
pip3 install cchardet
pip3 install aiodns

#deactivate

echo -e "\e[32mComplete!\e[0m" 
exit 0
