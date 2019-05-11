## Required packages:
* nginx
* python 3.6
* virtualenv + pip
* git

Ubuntu
sudo add-apt-repository pa:deadsnakes/ppa
sudo apt update
sudo apt install nginx git python36 python3.6-venv

## Nginx Virtual Host config
* see nginx.template.conf
* find replace DOMAIN w/ real domain name

## systemd Service
* see gunicorn-systemd.template.service
* replace DOMAIN with, eg.g, staging.my-domain.com

