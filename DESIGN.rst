Itabashi (板橋) Design
======================

Itabashi is made up of an IRC module and a Discord module, which pass events through a shared event manager. We call these modules that login and start passing messages from/to a communication service IM modules (Instant Messaging modules).

This architecture makes it fairly simple to create new IM modules, and to enable/disable IM modules as desired. All that's required is being able to run in parallel to the other IM modules currently running. The IRC and Discord modules do this by running through the asyncio event loop.


IM Modules
----------

IM Modules take the config dictionary and the shared event manager. They setup their required information from this config dict and attach to the message events dispatched by other IM modules.

When they receive a message, they dispatch an event through the event manager so that other IM Modules can catch and display these messages in their own formats. These dispatched events should contain separate elements such as `'channel'`, `'source'`, `'message'`, etc for other modules to handle and display as they see fit.


Logging
-------

Itabashi will eventually gain a logging system. This will work by choosing a uniform logging format, and then having all IM Modules output `'log'` events to be logged by a single centralised logger. This may require naming each channel-link, as logging messages will be output and forwarded to the appropriate link logs.
