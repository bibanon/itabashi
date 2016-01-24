# Written by Daniel Oaks <daniel@danieloaks.net>
from girc.formatting import escape, remove_formatting_codes
import girc


class IrcManager:
    def __init__(self, config, event_manager):
        self.config = config
        self.events = event_manager

        self.dispatch_channels = list(config['channelMapping'].values())
        self.channels = config['channelMapping']

        reactor = girc.Reactor()

        # register irc handlers
        reactor.register_event('in', 'raw', self.handle_reactor_raw_in, priority=1)
        reactor.register_event('out', 'raw', self.handle_reactor_raw_out, priority=1)
        reactor.register_event('in', 'pubmsg', self.handle_pubmsgs)

        # register itabashi handlers
        self.events.register('discord ready', self.handle_discord_ready)
        self.events.register('discord message', self.handle_discord_message)

        # setup connection
        self.irc = reactor.create_server('ita')
        self.irc.set_user_info(config['nickname'], user='ita')
        self.irc.join_channels(*list(config['channelMapping'].values()))
        self.irc.connect(config['server'], 6667)

    def handle_reactor_raw_in(self, event):
        print('irc:', event['server'].name, ' ->', escape(event['data']))

    def handle_reactor_raw_out(self, event):
        print('irc:', event['server'].name, '<- ', escape(event['data']))

    def handle_discord_ready(self, event):
        # don't actually dispatch messages here because that would be spammy
        #   and very, very annoying after a while
        return
        for channel in self.dispatch_channels:
            self.irc.msg(channel, 'Discord attached')

    def handle_discord_message(self, event):
        if event['channel'].name in self.channels:
            assembled_message = '$c[grey]<$r$b{}$b$c[grey]>$r {}'.format(escape(event['source'].name), escape(event['message']))
            self.irc.msg(self.channels[event['channel'].name], assembled_message)

    def handle_pubmsgs(self, event):
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
