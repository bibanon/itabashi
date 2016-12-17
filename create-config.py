#!/usr/bin/env python3
# create a config file for use with itabashi
from __future__ import print_function
import getpass
import json
import sys

if sys.version_info[0] < 3:
    in_func = raw_input
else:
    in_func = input

# using discord-irc/slack-irc format
config = {}

config['nickname'] = in_func('IRC Nickname: ')
config['server'] = in_func('IRC Server: ')
config['discordEmail'] = in_func('Discord Email: ')
config['discordPassword'] = getpass.getpass('Discord Password: ')

chans = {}
while True:
    print('Discord to IRC channel link - just hit enter to exit')
    discord_chan = in_func('Discord Channel: ').strip()
    irc_chan = in_func('IRC Channel: ').strip()

    if not (discord_chan and irc_chan):
        if len(chans) < 1:
            print('You need to have at least one channel link')
            continue
        else:
            break

    chans[discord_chan] = irc_chan

config['channelMapping'] = chans

with open('config.json', 'w') as f:
    json.dump([config], f, indent=2, sort_keys=True)

print('Config file has been dumped to config.json')
