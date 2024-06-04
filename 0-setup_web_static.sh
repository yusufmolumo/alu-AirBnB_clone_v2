#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Update and install nginx if it's not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update -y
    sudo apt-get install nginx -y
fi

# Create required directories if they don't already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create (or recreate) the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Ensure ubuntu user and group exist
if ! id -u ubuntu > /dev/null 2>&1; then
    sudo adduser --disabled-password --gecos "" ubuntu
fi

if ! getent group ubuntu > /dev/null 2>&1; then
    sudo addgroup ubuntu
fi

# Give ownership of /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
sudo sed -i '/server_name _;/a \ \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart || sudo service nginx start

exit 0
