#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['52.207.225.125', '54.160.166.220']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory
        put(archive_path, "/tmp/")

        # Extract archive to /data/web_static/releases/<archive filename without extension>
        archive_filename = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, folder_name))

        # Remove archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move contents of web_static/ to new folder
        run("mv {}/web_static/* {}".format(folder_name, folder_name))

        # Remove empty web_static/ directory
        run("rm -rf {}/web_static".format(folder_name))

        # Remove current symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
