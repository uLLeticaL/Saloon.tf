import re
import time
import settings, utilities
from SteamWeb import Authenticate, Community, Trade

saveData = utilities.DataHolder()
botLog = utilities.BotLog

print "Saloon.tf started. Write 'help' to get commands list."
for botID, bot in enumerate(settings.bots):
  if bot["autostart"]:
    print "Starting " + bot["name"] + " bot"
    Authenticate().signIn(botID)

while True:
  entered = raw_input(">>> ")
  arguments = entered.split()
  if len(arguments) > 1:
    botID = int(arguments[1])
    if len(settings.bots) > botID:
      bot = settings.bots[botID]
      if arguments[0] == "start":
        print "Starting " + str(settings.bots[botID]["name"]) + " bot"
        Authenticate().signIn(botID)
      elif bot["sessionid"]:
        if arguments[0] == "getFriends":
          Community().Friends(botID)
        elif arguments[0] == "addFriend":
          if len(arguments) == 3 and arguments[2].isdigit():
            Community().Friends(botID, steamID = arguments[2]).add()
        elif arguments[0] == "acceptFriend":
          if len(arguments) == 3 and arguments[2].isdigit():
            Community().Friends(botID, steamID = arguments[2]).accept()
        elif arguments[0] == "removeFriend":
          if len(arguments) == 3 and arguments[2].isdigit():
            Community().Friends(botID, steamID = arguments[2]).remove()
        elif arguments[0] == "getReceivedOffers":
            Trade().Offers(botID)
      else:
        botLog("Bot is not started.", botID)
    else:
      print "Couldn't find the bot with the specified id"
  elif arguments[0] == "exit":
    print "Exiting."
    break
  else:
    print "Entered wrong command."