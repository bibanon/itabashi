#!/usr/bin/python3
# create a config file for use with itabashi
from __future__ import print_function
import getpass
import json
import sys

from slugify import slugify

if sys.version_info[0] < 3:
    in_func = raw_input
else:
    in_func = input

# custom format, kept in line with a 'format' key
config = {
    'format': 1,
    'links': {},
    'modules': {
        'discord': {},
        'irc': {},
    },
}

config['modules']['discord']['email'] = in_func('Discord Email: ')
config['modules']['discord']['password'] = getpass.getpass('Discord Password: ')
config['modules']['irc']['nickname'] = in_func('IRC Nickname: ')
config['modules']['irc']['server'] = in_func('IRC Server: ')

print('Link Configuration')
print('To ignore a specific specific type of link, simply hit enter without specifying a name')
links = {}
while True:
    print()
    name = in_func('Link Name: ').strip()
    slug = slugify(name)
    log = in_func('Log this link [n]? ').strip()
    discord_chan = in_func('Discord Channel: ').strip()
    irc_chan = in_func('IRC Channel: ').strip()

    if slug in links:
        overwrite = in_func('Link with that name already exists, overwrite existing link [y]? ').strip()
        if len(overwrite) == 0 or overwrite[0].lower() in '1yt':
            pass
        else:
            print('Skipping link')
            continue

    if not (discord_chan and irc_chan):
        print('You need to have one Discord channel and one IRC channel to link together')
        continue

    if len(log) >= 1 and log[0].lower() in '1yt':
        log = True
        print('Logging link')
    else:
        log = False
        print('Will not log link')

    links[slug] = {
        'name': name,
        'log': log,
        'channels': {
            'discord': discord_chan,
            'irc': irc_chan,
        },
    }

    another_link = in_func('Setup another link [n]? ')
    if len(another_link) and another_link[0].lower() in '1yt':
        pass
    else:
        break

config['links'] = links

with open('config.json', 'w') as f:
    json.dump([config], f, indent=2, sort_keys=True)

print('Config file has been dumped to config.json')
