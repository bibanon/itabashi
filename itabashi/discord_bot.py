#!/usr/bin/python3
# Itabashi - quick and dirty discord bot
# itabashi_discord.py: discord bot
# Developed by Antonizoon for the Bibliotheca Anonoma

import discord
import logging
import json

# log all info messages
logging.basicConfig(level=logging.INFO)

class Itabashi(object):
	def __init__(self, config_fname='config.json'):
		# import config from JSON
		with open(config_fname, 'r') as f:
			self.config = json.load(f)
		
		discord_email = config[0]['discordEmail']
		discord_password = config[0]['discordPassword']
		self.discord_channel = 'bibanon-core'
		self.irc_channel = 'bibanon-core'
		
		# create a client
		self.client = discord.Client()
		self.client.login(discord_email, discord_password)

		# quit if not logged in
		if not self.client.is_logged_in:
			logging.info("Failed to login as %s." %s)
		
		# start the discord.py client
		client.run()

	# say hello to the message author
	@staticmethod
	def say_hello(message):
		text = 'Hello, %s' % message.author
		client.send_message(message.channel, text)
		logging.info('Sent message to %s - #%s (%s): %s' % (message.server.name, message.channel.name, message.channel.id, text))

	# send a message to IRC
	@staticmethod
	def irc_bridge(message):
		print('<%s> %s' % (message.author, message.content))
		logging.info('Sent message to IRC - #%s: <%s> %s' % (IRC_CHANNEL, message.author, message.content))

	@client.event
	def on_ready():
		print('Logged in as')
		print(client.user.name)
		print(client.user.id)
		print('------')
		
		# show all available channels and find the two channels to bridge
		print('Available Channels:')
		for channel in client.get_all_channels():
			print('#%s (%s)' % (channel.name, channel.id))
		
		print('------')

	@client.event
	def on_message(message):
		logging.info('Recieved - #%s: <%s> %s' % (message.channel.name, message.author, message.content))
		
		# for the #bibanon discord channel only
		if message.channel.name == DISCORD_CHANNEL:
			# say hello to test if the bot functions
			if message.content.startswith('!hello'):
				say_hello(message)
			
			# bridge messages to #bibanon-core channel (ignore your own messages of course)
			if str(message.author) != str(client.user.name):
				irc_bridge(message)

def main():
	# create an itabashi bridge object
	itabashi = Itabashi()

if __name__ == "__main__":
	main()