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
        self.client.event(self.on_message)

        # start the discord.py client
        @asyncio.coroutine
        def main_task():
            yield from self.client.login(email, password)
            yield from self.client.connect()
        asyncio.async(main_task())

    # say hello to the message author
    def say_hello(self, message):
        text = 'Hello, %s' % message.author
        client.send_message(message.channel, text)
        # logging.info('Sent message to %s - #%s (%s): %s' % (message.server.name, message.channel.name, message.channel.id, text))

    def handle_irc_message(self, event):
        chan = self.discord_channels[self.receive_irc_channels.get(event['channel'].name)]
        if chan:
            assembled_message = '<{}> {}'.format(event['source'].nick, event['message'])
            asyncio.async(self.client.send_message(chan, assembled_message))

    @asyncio.coroutine
    def on_ready(self):
        print('Logged in as')
        print(self.client.user.name)
        print(self.client.user.id)
        print('------')

        # show all available channels and find the two channels to bridge
        print('Available Discord Channels:')
        for channel in self.client.get_all_channels():
            print('#%s (%s)' % (channel.name, channel.id))
            if channel.name in self.dispatch_channels:
                self.discord_channels[channel.name] = channel

        print('------')

        self.events.dispatch('discord ready', {})

    @asyncio.coroutine
    def on_message(self, message):
        # logging.info('discord - recieved message - #%s: <%s> %s' % (message.channel.name, message.author, message.content))

        # for our discord channel only
        if message.channel.name.lower() in self.dispatch_channels:
            # say hello to test if the bot functions
            if message.content.startswith('!hello'):
                self.say_hello(message)

            # bridge messages to the irc channel (ignore your own messages of course)
            if str(message.author) != str(self.client.user.name):
                # logging.info('Sent message to IRC - #%s: <%s> %s' % (IRC_CHANNEL, message.author, message.content))
                info = {
                    'type': 'message',
                    'service': 'discord',
                    'channel': message.channel,
                    'source': message.author,
                    'message': message.content,
                }

                self.events.dispatch('discord message', info)
