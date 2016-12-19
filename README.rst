Itabashi (板橋) - Discord-IRC Bridge
====================================

**Itabashi** is a bot that syncs messages between a Discord and an IRC channel. It is written in Python, using the `discord.py <https://github.com/Rapptz/discord.py>`_ and `gIRC <https://github.com/DanielOaks/girc>`_ libraries.

Itabashi was developed by the Bibliotheca Anonoma to coordinate operations between its Discord and IRC channels.

Dependencies
------------

* python3.4 (with venv)
* gcc
* libffi + development libraries

Debian/Ubuntu:
::
    sudo apt-get install python3.4 python3.4-venv gcc libffi-dev

Fedora:
:: 
    # dnf install python3 gcc libffi libffi-devel

Red Hat/CentOS:

Install Python34 as specified in this link: https://www.softwarecollections.org/en/scls/rhscl/rh-python34/

You will also need to fix the python34 package for pip as Red Hat forgot to include some files: http://stackoverflow.com/a/33767179

Setup
-----

> **Note**: Itabashi requires Python 3.4 or above, as it uses the ``asyncio`` library.

Clone the repository and enter the folder:
::
    $ git clone https://github.com/bibanon/itabashi.git
    $ cd itabashi

Create a virtualenv and use it (this makes sure that your various installed packages don't conflict system-wide):
::
    $ python3 -m venv env # for Debian/Ubuntu
    $ pyvenv env          # for Fedora/CentOS/RHEL
    $ source env/bin/activate

Install the dependencies:
::
    $ pip3 install -r requirements.txt

Create a configuration file:
::
    $ python3 create-config.py

Start using the bot!
::
    $ python3 startlink.py connect

The bot will then connect to both IRC and Discord using the provided credentials and start relaying messages.

Systemd Daemon User
-------------------

We can also create a systemd daemon user to control the bot.
::
    $ cd /home
    # git clone https://github.com/bibanon/itabashi.git
    # useradd -s /bin/bash -d /home/itabashi -r itabashi
    # chown -R itabashi:itabashi /home/itabashi

Then, set up the discord bot as usual, but as the daemon user. 
::
    # sudo -i -u itabashi
    $ python3 -m venv env
    $ source env/bin/activate
    $ pip3 install -r requirements.txt
    $ python3 create-config.py

Finally, use the command below to create a service.sh file for the systemd service to use:
::
    $ nano /home/itabashi/service.sh

Put the following lines inside that file:
::
    #!/bin/bash
    # Systemd Service launcher for Itabashi that runs in Python virtualenv.
    source env/bin/activate
    python3 startlink.py connect

Then finish up by making that script executable, exit the daemon user, and disable login for the daemon user:
::
    $ chmod +x /home/itabashi/service.sh
    $ exit
    # chsh -s /bin/false itabashi

Now we can create a systemd service file to use:

/etc/systemd/system/itabashi.service
::
    [Unit]
    Description=Itabashi Discord/IRC Bridge
    After=multi-user.target
    
    [Service]
    ExecStart=/home/itabashi/service.sh
    
    WorkingDirectory=/home/itabashi/
    
    User=itabashi
    Group=itabashi
    
    [Install]
    WantedBy=multi-user.target

To start or stop the discord bridge, use these commands:
::
    # systemctl restart itabashi
    # systemctl stop itabashi

To enable the service at every boot, use this command:
::
    # systemctl enable itabashi

License
-------

Copyright (C) 2016 Bibliotheca Anonoma

This file is part of Itabashi.

Itabashi is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

Itabashi is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Itabashi. If not, see <http://www.gnu.org/licenses/>.
