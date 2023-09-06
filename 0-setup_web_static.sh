#!/usr/bin/env bash
#setting up servers#

if ! command -v nginx &> /dev/null;
then
    sudo apt-get -y update
    sudo apt-get install -y nginx
    sudo service nginx start
fi

sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "
<html>
  <head>
  </head>
  <body>
    dynamikservices
  </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR ubuntu:ubuntu /data/

sudo sed -i '/server_name _;/a \\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx restart
