# Written by Daniel Oaks <daniel@danieloaks.net>
from girc.formatting import escape
import girc


class IrcManager:
    def __init__(self, config, event_manager):
        self.config = config
        self.events = event_manager

        reactor = girc.Reactor()

        # register irc handlers
        reactor.register_event('in', 'raw', self.handle_reactor_raw_in, priority=1)
        reactor.register_event('out', 'raw', self.handle_reactor_raw_out, priority=1)

        # register itabashi handlers
        self.events.register('discord message', self.handle_discord_message)

        # setup connection
        irc = reactor.create_server('ita')
        irc.set_user_info(config['nickname'], user='ita')
        irc.join_channels(*list(config['channelMapping'].values()))
        irc.connect(config['server'], 6667)

    def handle_reactor_raw_in(self, event):
        print('irc:', event['server'].name, ' ->', escape(event['data']))

    def handle_reactor_raw_out(self, event):
        print('irc:', event['server'].name, '<- ', escape(event['data']))

    def handle_discord_message(self, event):
        print('discord: GOT A MESSAGE', event)
