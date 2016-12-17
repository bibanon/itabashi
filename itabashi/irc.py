# Written by Daniel Oaks <daniel@danieloaks.net>
import itabashi

from girc.formatting import escape, remove_formatting_codes
import girc


class IrcManager:
    def __init__(self, logger, config, event_manager):
        self.logger = logger
        self.config = config
        self.events = event_manager

        self.dispatch_channels = list(config['channelMapping'].values())
        self.channels = config['channelMapping']

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
        self.irc.set_user_info(config['nickname'], user='ita')
        self.irc.join_channels(*list(config['channelMapping'].values()))
        if 'nickservPassword' in config:
            self.irc.nickserv_identify(config['nickservPassword'])
        self.irc.connect(config['server'], 6667)

        self.logger.info('irc: Started and connected to {}/{}'.format(config['server'], 6667))

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
        if event['channel'].name in self.channels:
            assembled_message = '$c[grey]<$r$b{}$b$c[grey]#{}>$r {}'.format(escape(event['source'].name), escape(event['source'].discriminator), escape(event['message']))
            self.irc.msg(self.channels[event['channel'].name], assembled_message)
