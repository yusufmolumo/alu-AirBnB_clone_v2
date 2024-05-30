#!/usr/bin/env bash
# Install Nginx if not already installed
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx

# create folders
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
#create a fake html file
echo "This is a test" | sudo tee /data/web_static/releases/test/index.html
# create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx start
