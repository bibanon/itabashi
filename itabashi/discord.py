# Itabashi - quick and dirty discord bot
# itabashi_discord.py: discord bot
# Developed by Antonizoon for the Bibliotheca Anonoma
import asyncio
import sys

import aiohttp
import discord
import websockets
from italib import backoff

loop = asyncio.get_event_loop()


class DiscordManager:
    def __init__(self, logger, config, event_manager):
        self.logger = logger
        self.config = config
        self.events = event_manager

        self.dispatch_channels = list(config['channelMapping'].keys())
        self.receive_irc_channels = {v: k for k, v in config['channelMapping'].items()}
        self.discord_channels = {}

        self.events.register('irc message', self.handle_irc_message)
        self.events.register('irc action', self.handle_irc_action)

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
            # guided by https://gist.github.com/Hornwitser/93aceb86533ed3538b6f
            # thanks Hornwitser!
            retry = backoff.ExponentialBackoff()

            # login to Discord
            while True:
                try:
                    yield from self.client.login(email, password)
                except (discord.HTTPException, aiohttp.ClientError):
                    logging.exception("discord.py failed to login, waiting and retrying")
                    yield from asyncio.sleep(retry.delay())
                else:
                    break

            # connect to Discord and reconnect when necessary
            while self.client.is_logged_in:
                if self.client.is_closed:
                    self.client._closed.clear()
                    self.client.http.recreate()

                try:
                    yield from self.client.connect()

                except (discord.HTTPException, aiohttp.ClientError,
                        discord.GatewayNotFound, discord.ConnectionClosed,
                        websockets.InvalidHandshake,
                        websockets.WebSocketProtocolError) as e:
                    if isinstance(e, discord.ConnectionClosed) and e.code == 4004:
                        raise # Do not reconnect on authentication failure
                    logging.exception("discord.py disconnected, waiting and reconnecting")
                    yield from asyncio.sleep(retry.delay())

        # actually start running the client
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

    # dispatching messages
    @asyncio.coroutine
    def on_message(self, message):
        # for our watched channels only
        self.logger.debug('discord: raw 1')
        if message.channel.name.lower() in self.dispatch_channels:
            self.logger.debug('discord: raw 2')
            # dispatch all but our own messages
            if str(message.author) != str(self.client.user):
                self.logger.debug('discord: raw 3 - dispatching')
                full_message = [message.clean_content]
                if not full_message[0]:
                    full_message.pop(0)
                for attachment in message.attachments:
                    full_message.append(attachment.get('url', 'No URL for attachment'))

                info = {
                    'type': 'message',
                    'service': 'discord',
                    'channel': message.channel,
                    'source': message.author,
                    'message': ' '.join(full_message),
                }

                self.events.dispatch('discord message', info)

    # receiving messages
    def handle_irc_message(self, event):
        chan = self.discord_channels[self.receive_irc_channels.get(event['channel'].name)]
        if chan:
            assembled_message = '**<{}>** {}'.format(event['source'].nick, event['message'])
            asyncio.async(self.client.send_message(chan, assembled_message))

    def handle_irc_action(self, event):
        chan = self.discord_channels[self.receive_irc_channels.get(event['channel'].name)]
        if chan:
            assembled_message = '**\\* {}** {}'.format(event['source'].nick, event['message'])
            asyncio.async(self.client.send_message(chan, assembled_message))
