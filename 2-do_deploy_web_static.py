#!/usr/bin/python3
# script that distributes an archive to web servers
from fabric.api import env, put, run, sudo
from os.path import exists, isdir, basename, splitext
import re

# Set the username and host for SSH connection to the server
env.user = 'ubuntu'
env.hosts = ['54.207.225.125', '54.160.166.220']
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Distributes archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Extract the file name without extension
        filename = basename(archive_path)
        no_ext = splitext(filename)[0]
        folder = "/data/web_static/releases/{}".format(no_ext)

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Create the release folder if it doesn't exist
        run("mkdir -p {}".format(folder))

        # Uncompress the archive to the folder
        run("tar -xzf /tmp/{} -C {}".format(filename, folder))

        # Remove the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move all files from web_static to the new folder
        run("mv {}/web_static/* {}".format(folder, folder))

        # Remove the web_static folder
        run("rm -rf {}/web_static".format(folder))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(folder))

        # Ensure the 'hbnb_static' directory exists and sync with 'current'
        run("sudo mkdir -p /var/www/html/hbnb_static")
        run("sudo cp -r /data/web_static/current/* /var/www/html/hbnb_static/")

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False

# Usage:
# fab -f 2-do_deploy_web_static.py do_deploy:/path/to/file.tgz
