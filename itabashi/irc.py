# Written by Daniel Oaks <daniel@danieloaks.net>
import ssl

from girc.formatting import escape, remove_formatting_codes
import girc

import itabashi


class IrcManager:
    def __init__(self, logger, config, event_manager):
        self.logger = logger
        self.config = config
        self.events = event_manager

        self.dispatch_channels = [config['links'][name]['channels']['irc'] for name in config['links'] if 'irc' in config['links'][name]['channels']]
        # simplifies down to a simple list of Discord chans -> IRC chans
        self.channels = {
            'discord': {},
        }
        for name in config['links']:
            link = config['links'][name]['channels']
            if 'discord' in link and 'irc' in link:
                if link['discord'] not in self.channels['discord']:
                    self.channels['discord'][link['discord']] = []
                if link['irc'] not in self.channels['discord'][link['discord']]:
                    self.channels['discord'][link['discord']].append(link['irc'])

        reactor = girc.Reactor()

        # register irc handlers
        reactor.register_event('in', 'raw', self.handle_reactor_raw_in, priority=1)
        reactor.register_event('out', 'raw', self.handle_reactor_raw_out, priority=1)
        reactor.register_event('in', 'ctcp', self.handle_reactor_ctcp)
        reactor.register_event('in', 'pubmsg', self.handle_reactor_pubmsgs)
        reactor.register_event('in', 'pubaction', self.handle_reactor_pubactions)

        # register itabashi handlers
        self.events.register('discord ready', self.handle_discord_ready)
        self.events.register('discord disconnected', self.handle_discord_disconnected)
        self.events.register('discord message', self.handle_discord_message)

        # setup connection
        self.irc = reactor.create_server('ita')
        self.irc.set_user_info(config['modules']['irc']['nickname'], user='ita')
        self.irc.join_channels(*[config['links'][name]['channels']['irc'] for name in config['links'] if 'irc' in config['links'][name]['channels']])
        if 'nickserv_password' in config['modules']['irc']:
            self.irc.nickserv_identify(config['modules']['irc']['nickserv_password'])

        use_tls = config['modules']['irc']['tls']
        if use_tls and not config['modules']['irc']['tls_verify']:
            use_tls = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            use_tls.verify_mode = ssl.CERT_NONE

        self.irc.connect(config['modules']['irc']['server'], config['modules']['irc']['port'], ssl=use_tls)

        self.logger.info('irc: Started and connected to {}/{}'.format(
            config['modules']['irc']['server'], config['modules']['irc']['port']))

    # display
    def handle_reactor_raw_in(self, event):
        try:
            self.logger.debug('raw irc: {}  -> {}'.format(event['server'].name, escape(event['data'])))
        except (UnicodeDecodeError, UnicodeEncodeError):
            self.logger.debug('raw irc: {}  -> {}'.format(event['server'].name, 'Data coule not be displayed'))

    def handle_reactor_raw_out(self, event):
        try:
            self.logger.debug('raw irc: {} <-  {}'.format(event['server'].name, escape(event['data'])))
        except (UnicodeDecodeError, UnicodeEncodeError):
            self.logger.debug('raw irc: {} <-  {}'.format(event['server'].name, 'Data could not be displayed'))

    # VERSION and such
    def handle_reactor_ctcp(self, event):
        if event['ctcp_verb'] == 'version':
            event['source'].ctcp_reply('VERSION', 'Itabashi (板橋)/{}'.format(itabashi.__version__))
        elif event['ctcp_verb'] == 'source':
            event['source'].ctcp_reply('SOURCE', 'https://github.com/bibanon/itabashi')
        elif event['ctcp_verb'] == 'clientinfo':
            event['source'].ctcp_reply('CLIENTINFO', 'ACTION CLIENTINFO SOURCE VERSION')

    # dispatching messages
    def handle_reactor_pubmsgs(self, event):
        if event['source'].is_me:
            return
        if event['target'].name in self.dispatch_channels:
            info = {
                'type': 'message',
                'service': 'irc',
                'channel': event['channel'],
                'source': event['source'],
                'message': remove_formatting_codes(event['message']),
            }

            self.events.dispatch('irc message', info)

    def handle_reactor_pubactions(self, event):
        if event['source'].is_me:
            return
        if event['target'].name in self.dispatch_channels:
            info = {
                'type': 'message',
                'service': 'irc',
                'channel': event['channel'],
                'source': event['source'],
                'message': remove_formatting_codes(event['message']),
            }

            self.events.dispatch('irc action', info)

    # receiving messages
    def handle_discord_ready(self, event):
        # don't actually dispatch messages here because that would be spammy
        #   and very, very annoying after a while
        return
        for channel in self.dispatch_channels:
            self.irc.msg(channel, 'Discord attached')

    def handle_discord_disconnected(self, event):
        for channel in self.dispatch_channels:
            self.irc.msg(channel, 'Discord disconnected')

    def handle_discord_message(self, event):
        assembled_message = '$c[grey]<$r$b{}$b$c[grey]#{}>$r {}'.format(escape(event['source'].name), escape(event['source'].discriminator), escape(event['message']))
        for chan in self.channels['discord'].get(event['channel'].name, []):
            self.irc.msg(chan, assembled_message)
