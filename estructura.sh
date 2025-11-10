#!/bin/bash

PROJECT="ansible-system-monitor"

mkdir -p $PROJECT/inventories
mkdir -p $PROJECT/playbooks
mkdir -p $PROJECT/roles/flask-app/tasks
mkdir -p $PROJECT/roles/flask-app/templates
mkdir -p $PROJECT/roles/flask-app/files/app

touch $PROJECT/inventories/hosts.ini
touch $PROJECT/playbooks/deploy.yml
touch $PROJECT/roles/flask-app/tasks/main.yml
touch $PROJECT/roles/flask-app/templates/flask.service.j2
touch $PROJECT/roles/flask-app/files/app/app.py
touch $PROJECT/roles/flask-app/files/app/system_info.py
touch $PROJECT/roles/flask-app/files/app/requirements.txt

echo "Estructura de proyecto creada en ./$PROJECT"
