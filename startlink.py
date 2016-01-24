#!/usr/bin/env python3
# Written by Daniel Oaks <daniel@danieloaks.net>
"""startlink.py - Itabashi Discord-IRC linker.

Usage:
    startlink.py connect
    startlink.py --version
    startlink.py (-h | --help)

Options:
    connect        Connect to the Discord and IRC channels.
    --version      Show the running version of Itabashi.
    (-h | --help)  Show this message.
"""
import json
import os
import sys
import asyncio

import itabashi

from docopt import docopt
from girc.ircreactor.events import EventManager

if __name__ == '__main__':
    arguments = docopt(__doc__, version=itabashi.__version__)

    if arguments['connect']:
        if not os.path.exists('config.json'):
            print('Config file does not exist, run create-config.py')
            sys.exit(1)
        with open('config.json', 'r') as config_file:
            config = json.loads(config_file.read())[0]

        events = EventManager()

        irc = itabashi.IrcManager(config, events)

        asyncio.get_event_loop().run_forever()
