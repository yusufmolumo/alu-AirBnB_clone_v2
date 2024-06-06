#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric import Connection, task
from os.path import exists

# Define the list of servers
servers = ['52.207.225.125', '54.160.166.220']

@task(hosts=servers)
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        # Extract filename and folder name
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to /tmp/
        c.put(archive_path, '/tmp/')

        # Create the directory if it doesn't exist
        c.run('mkdir -p {}{}/'.format(path, folder_name))

        # Uncompress the archive
        c.run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, folder_name))

        # Remove the archive
        c.run('rm /tmp/{}'.format(file_name))

        # Move files from web_static to new folder
        c.run('mv {0}{1}/web_static/* {0}{1}/'.format(path, folder_name))

        # Remove web_static folder
        c.run('rm -rf {}{}/web_static'.format(path, folder_name))

        # Remove the old symbolic link
        c.run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        c.run('ln -s {}{}/ /data/web_static/current'.format(path, folder_name))

        return True
    except Exception as e:
        print(e)
        return False
