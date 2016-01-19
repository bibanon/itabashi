Design (Method 1: ZeroMQ) 
========================

Itabashi is made up of two bots for Discord and IRC (respectively), which could communicate with each other via ZeroMQ Request/Response sockets. A third, unrelated IRC Logger would be keeping track of messages.

This would no longer need a database, especially as SQLite can get hairy with two active processes.

## ZeroMQ

https://www.digitalocean.com/community/tutorials/how-to-work-with-the-zeromq-messaging-library

## Discord Bot: `itabashi_discord.py`

The Discord Bot uses the [discord.py](https://github.com/Rapptz/discord.py) API wrapper.

* Outbound (From Discord to IRC)
  * Connect to the Discord channel.
  * Wait for a message notification from the Discord server.
  * When recieved, relay the message over to the IRC Bot using `pyzmq`.
    * Obviously, the bot will ignore messages that it made itself.
  * Wait for confirmation from the IRC bot. If the bot does not respond within an interval, cache the notification.
  * When the IRC Bot returns, send all recent messages.
* Inbound (From IRC to Discord)
  * Wait for a message notification from the IRC Bot.
  * When recieved, post the message to Discord.

## IRC Bot: `itabashi_irc.py`

* Outbound (From IRC to Discord)
  * Connect to the IRC Server and join a channel.
    * Nickserv authentication can be used if necessary.
  * Monitor the channel for any new messages.
  * When recieved, relay the message over to the Discord Bot using `pyzmq`.
    * Obviously, the bot will ignore messages that it made itself.
  * Wait for confirmation from the Discord bot. If the bot does not respond within an interval, cache the notification.
  * When the IRC Bot returns, send all recent messages.
* Inbound (From Discord to IRC)
  * Wait for a message notification from the Discord Bot.
  * When recieved, post the message to IRC Bot.

## IRC Logger

The IRC Logger should be customized to convert the IRC bot's messages to normal user messages when outputting them.

Design (Method 2: SQLite Database)
==================================

Itabashi is made up of two bots for Discord and IRC (respectively) that store messages in a single SQLite database. However, there can be scalability problems when two connections are being made at the same time between the two.

## Discord Bot: `itabashi_discord.py`

The Discord Bot uses the [discord.py](https://github.com/Rapptz/discord.py) API wrapper.

* Outbound (From Discord to IRC)
  * Connect to the Discord channel.
  * Wait for a message notification from the Discord server.
  * When recieved, log the message in the SQLite Database.
    * Obviously, the bot will ignore messages that it made itself.
* Inbound (From IRC to Discord)
  * Watch the SQLite database for any new records made since the bot last posted.
  * When recieved, post the message to Discord.