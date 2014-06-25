### Daemon
Daemon is a Steam bot used for items withdrawals and deposits using web interfaces.
##### SteamWeb.py
SteamWeb.py is the generic module for interacting with Steam servers. It contains definitions for Bot, Friend and Offer objects and the functions to interact with them.
##### Daemon.py
Daemon.py is the bot's daemon which looks for new offers, checks if they are correct and add items to the databse. It also manages the queue and interacts with the website through the websocket connection on port 9000
##### Other modules
__bots.py__ is the proof of concept cli script or interacting with the bot. It can be used to debug potential problems with SteamWeb.py by manually controlling the bot.  
__database.py__ is the SQLAlchemy's database model containing object for each of the table. It's also used by the website.  
__settings.py__ is the simple settings file where you can set which bot should start as default, enter the api key or database data.  
__utilities.py__ is the module for everything else which can be shared between the Website, SteamWeb.py or the Daemon but isn't complex enough to have it's own module.
