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

```
sudo apt-get install python3.4 python3.4-venv gcc libffi-dev
```

Fedora:

```
sudo dnf install python3 gcc libffi libffi-devel
```

Setup
-----

> **Note**: Itabashi requires Python 3.4 or above, as it uses the ``asyncio`` library.

Clone the repository and enter the folder:

    $ git clone https://github.com/bibanon/itabashi.git

    $ cd itabashi

Create a virtualenv and use it (this makes sure that your various installed packages don't conflict system-wide):

    $ python3 -m venv env # for Debian/Ubuntu
    
    $ pyvenv env          # for Fedora/CentOS/RHEL

    $ source env/bin/activate

Install the dependencies:

    $ pip3 install -r requirements.txt

Create a configuration file:

    $ python3 create-config.py

Start using the bot!

    $ python3 startlink.py connect

The bot will then connect to both IRC and Discord using the provided credentials and start relaying messages.


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
