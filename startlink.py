#!/usr/bin/env python3
# Written by Daniel Oaks <daniel@danieloaks.net>
"""startlink.py - Itabashi Discord-IRC linker.

Usage:
    startlink.py connect [--log=<log>]
    startlink.py --version
    startlink.py (-h | --help)

Options:
    connect        Connect to the Discord and IRC channels.
    --log=<log>    Log to the specified filename [default: itabashi.log].
    --version      Show the running version of Itabashi.
    (-h | --help)  Show this message.
"""
import asyncio
import json
import logging
import os
import sys

from docopt import docopt
from girc.ircreactor.events import EventManager

import italib
import itabashi

if __name__ == '__main__':
    arguments = docopt(__doc__, version=itabashi.__version__)

    if arguments['connect']:
        if not os.path.exists('config.json'):
            print('Config file does not exist, run create-config.py')
            sys.exit(1)
        with open('config.json', 'r') as config_file:
            config = json.loads(config_file.read())[0]

        logging.basicConfig(filename=arguments['--log'], level=logging.DEBUG)
        logger = logging
        logger.info('Logger started')

        # check config version
        if config.get('version', 0) < italib.CURRENT_CONFIG_VERSION:
            #TODO(dan): automagic config file updating
            logger.fatal('Config format is too old, please update it.')
            print('Config format is too old, please update it.')
            exit(1)

        events = EventManager()

        irc = itabashi.IrcManager(logger, config, events)
        discord = itabashi.DiscordManager(logger, config, events)

        logger.debug('Itabashi events: {}'.format(events.events))

        asyncio.get_event_loop().run_forever()
