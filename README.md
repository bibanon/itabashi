板橋 (Itabashi) - Basic Discord-IRC Bridge
===========================================

> **Note:** Only the discord bot component is finished, and it just relays the message to `stdout`. The IRC Bot is not finished yet.

**板橋 (Itabashi)** is a bot that syncs messages between a Discord and an IRC channel. It is written in Python and uses the [discord.py](https://github.com/Rapptz/discord.py) API wrapper.

Itabashi was developed by the Bibliotheca Anonoma to coordinate operations between its Discord and IRC channels. Originally, we used [Discord-IRC](https://github.com/reactiflux/discord-irc) (a port of [Slack-IRC](https://github.com/ekmartin/slack-irc)), but it was too RAM-hungry and buggy to be viable.

## Create bot user

First, you will need to create the discord bot user and invite it to the discord channel to be bridged. 

An IRC user is not necessary, but recommended.

## Setup

> **Note**: Itabashi is explicitly designed for Python 3, though it may work on Python 2.

First, install the dependencies:

```
pip3 install discord.py 
```

Next, clone this repository to the current directory, and enter the folder:

```
git clone https://github.com/bibanon/itabashi
cd itabashi
```

You will want to create a configuration file (it's in JSON format so you can edit it by hand later on), so run the following program:

```
python3 create-config.py
```

Finally, run the bot itself with a configuration file as the parameter (if no argument is given, it will use `config.json` in the current directory).

```
python3 itabashi/discord_bot.py config.json
```

## License

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