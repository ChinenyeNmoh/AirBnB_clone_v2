#!/usr/bin/python3
"""Fabric script to delete out-of-date archives."""
from fabric.api import local, run, env
import os

env.hosts = ['100.24.255.208', '34.229.66.208']
env.user = 'ubuntu'


def do_clean(number=0):
    """Delete out-of-date archives."""
    try:
        number = int(number)
        if number < 1:
            number = 1

        # List all files in the versions folder
        files = sorted(os.listdir("versions"))
        files_to_delete = files[:-number]

        # Delete unnecessary archives in the versions folder
        for file in files_to_delete:
            local("rm -f versions/{}".format(file))

        # List all files in the /data/web_static/releases folder on both servers
        with cd("/data/web_static/releases"):
            files = run("ls -1").split()
            files_to_delete = files[:-number]

        # Delete unnecessary archives in the /data/web_static/releases folder on both servers
        for file in files_to_delete:
            run("rm -rf /data/web_static/releases/{}".format(file))

        return True

    except ValueError:
        return False

