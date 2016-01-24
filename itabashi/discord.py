# Itabashi - quick and dirty discord bot
# itabashi_discord.py: discord bot
# Developed by Antonizoon for the Bibliotheca Anonoma
import asyncio
import sys

import discord


class DiscordManager:
    def __init__(self, config, event_manager):
        self.config = config
        self.events = event_manager

        self.dispatch_channels = list(config['channelMapping'].keys())
        self.receive_irc_channels = {v: k for k, v in config['channelMapping'].items()}
        self.discord_channels = {}

        self.events.register('irc message', self.handle_irc_message)

        # extract values we use from config
        email = config['discordEmail']
        password = config['discordPassword']

        # create a client
        self.client = discord.Client()

        # attach events
        self.client.event(self.on_ready)
        self.client.event(self.on_socket_closed)
        self.client.event(self.on_message)

        # start the discord.py client
        @asyncio.coroutine
        def main_task():
            yield from self.client.login(email, password)
            yield from self.client.connect()
        asyncio.async(main_task())

    # retrieve channel objects we use to send messages
    @asyncio.coroutine
    def on_ready(self):
        print('Logged in as')
        print(self.client.user.name)
        print(self.client.user.id)
        print('------')

        # show all available channels and fill out our internal lists
        print('Available Discord Channels:')
        for channel in self.client.get_all_channels():
            print('#%s (%s)' % (channel.name, channel.id))
            if channel.name in self.dispatch_channels:
                self.discord_channels[channel.name] = channel

        print('------')

        self.events.dispatch('discord ready', {})

    @asyncio.coroutine
    def on_socket_closed(self):
        self.events.dispatch('discord disconnected', {})

    # dispatching messages
    @asyncio.coroutine
    def on_message(self, message):
        # for our watched channels only
        print('Raw message from Discord 1')
        if message.channel.name.lower() in self.dispatch_channels:
            print('Raw message from Discord 2')
            # dispatch all but our own messages
            if str(message.author) != str(self.client.user.name):
                print('Got a message from Discord, dispatching')
                info = {
                    'type': 'message',
                    'service': 'discord',
                    'channel': message.channel,
                    'source': message.author,
                    'message': message.content,
                }

                self.events.dispatch('discord message', info)

    # receiving messages
    def handle_irc_message(self, event):
        chan = self.discord_channels[self.receive_irc_channels.get(event['channel'].name)]
        if chan:
            assembled_message = '**<{}>** {}'.format(event['source'].nick, event['message'])
            asyncio.async(self.client.send_message(chan, assembled_message))
