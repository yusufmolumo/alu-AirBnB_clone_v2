from fabric.api import env, run, put, sudo
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        archive_name = archive_path.split("/")[-1]
        archive_folder = archive_name.split(".")[0]
        remote_tmp_path = "/tmp/{}".format(archive_name)
        releases_path = "/data/web_static/releases/{}".format(archive_folder)
        
        put(archive_path, remote_tmp_path)

        # Uncompress the archive to the folder
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(remote_tmp_path, releases_path))

        # Remove the archive from the web server
        run("rm {}".format(remote_tmp_path))

        # Move contents to the right folder
        run("mv {}/web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}/web_static".format(releases_path))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(releases_path))

        return True
    except Exception as e:
        print(e)
        return False
