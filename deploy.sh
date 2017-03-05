#!/usr/bin/env bash

# deploy django application
echo -e "\e[32mDeploy django application\e[0m"
bash deploy/deploy_django_project.sh

echo -e "\e[32mComplete!\e[0m"
exit 0
