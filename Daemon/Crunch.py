import re, time, json
import gmail
import database as db
import colorama as color
import threading
import SteamWeb

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

RBots = db.Session.query(db.Bots).all()
RItems = db.Session.query(db.Items).all()
items = {}
for RItem in RItems:
  classID = str(RItem.classID)
  items[classID] = RItem

class SteamWebCallback(object):
  def __init__(self, RBot):
    self.RBot = RBot

  def log(self, name, message):
    print color.Fore.BLUE + color.Style.BRIGHT + "[" + self.Bot.name + "] " + color.Fore.RESET + color.Style.RESET_ALL + message

  def steamGuard(self):
    # Manual authentication
    if self.RBot.emailPassword is None:
      while True:
        self.log("GuardCode sent to " + self.RBot.emailAddress)
        guardCode = raw_input(color.Fore.BLUE + color.Style.BRIGHT + "[" + self.Bot.name + "] " + color.Fore.RESET + color.Style.RESET_ALL + "GuardCode: ")
        return guardCode
    else:
      g = gmail.login(self.RBot.emailAddress, self.RBot.emailPassword)
      # Check for emails until we get Steam Guard code
      for i in range(0, 3):
        mails = g.inbox().mail(sender="noreply@steampowered.com", unread=True)
        if mails:
          mail = mails[-1]
          mail.fetch()
          guardCode = re.findall(r"log in again: ([A-Z0-9]{5})", mail.body)[0]
          mail.read()
          mail.delete()
          g.logout()
          return guardCode
        else:
          self.log(Bot.name, "Don't have any new emails")
          self.log(Bot.name, "Retrying in 3 seconds")
          time.sleep(3)
      self.log(Bot.name, "GuardCode sent to " + self.RBot.emailAddress + ". You'll have to manually enter the code.")
      guardCode = raw_input(color.Fore.BLUE + color.Style.BRIGHT + "[" + self.Bot.name + "] " + color.Fore.RESET + color.Style.RESET_ALL + "GuardCode: ")
      return guardCode

  def captchaCode(self, gid):
    # "Never give up on your goals, stay focused on your own"
    self.log(Bot.name, "Captcha needed. Saving it to the " + captchaPath)
    captchaPath = "captchas/" + self.RBot.name + "-" + response[u"captcha_gid"] + ".png"
    captcha = self.Bot.browser.open("https://steamcommunity.com/public/captcha.php?gid=" + gid).read()
    captchaFile = open(captchaPath, 'wb')
    captchaFile.write(captcha)
    captchaFile.close()
    captchaCode = raw_input(color.Fore.BLUE + color.Style.BRIGHT + "[" + self.Bot.name + "] " + color.Fore.RESET + color.Style.RESET_ALL + "Captcha: ")
    return captchaCode

class OfferHandler(object):
  def __init__(self, Bot, RBot):
    partners = {}
    offers = Bot.Trade().GetOffers()
    accepted = False
    if offers is not False:
      if len(offers) > 0:
        # Rework the dictionary to partner => offers
        for offerID in offers:
          offer = offers[offerID]
          steamID = offer.Partner.steamID
          if steamID in partners:
            partners[steamID].append(offer)
          else:
            partners[steamID] = [offer]
        steamIDs = partners.keys()

        RUsers = db.Session.query(db.Users).filter(db.Users.steamID.in_(steamIDs)).all()
        for RUser in RUsers:
          for offer in partners[str(RUser.steamID)]:
            if self.offerType(offer) is "Deposit":
              success = self.Deposit(offer, RUser)
            elif self.offerType(offer) is "Withdrawal":
              if RUser.steamID not in queue[Bot.id]:
                success = False
              else:
                success = self.Withdraw(offer, RUser)
            else:
              offer.decline()
              success = False

            if success:
              accepted = True
              Bot.log("Accepted trade #" + str(offer.offerID) + " from " + RUser.name + ".")
              if RUser.steamID in listeners:
                jsonString = json.dumps(["accepted"])
                listeners[RUser.steamID].sendMessage(jsonString)
              if RUser.steamID in queue[Bot.id]:
                QueueHandler().timeout(Bot.id, steamID)
            else:
              Bot.log("Trade #" + str(offer.offerID) + " had invalid items and was declined.")
              if RUser.steamID in listeners:
                jsonString = json.dumps(["declined"])
                listeners[RUser.steamID].sendMessage(jsonString)
          del partners[str(RUser.steamID)]

        for steamID in partners:
          Bot.log("User with SteamID: " + str(steamID) + " isn't registered yet. Declining his offers.")
          for offer in partners[steamID]:
            offer.decline()
        if accepted:
          db.Session.commit()

  def offerType(self, offer):
    if offer.itemsToReceive and not offer.itemsToGive:
      return "Deposit"
    elif offer.itemsToGive and not offer.itemsToReceive:
      return "Withdrawal"
    else:
      return False

  def Deposit(self, offer, RUser):
    metal = 0
    correctItems = []
    for item in offer.itemsToReceive:
      if item[1] in items:
        RItem = items[item[1]]
        if RItem.metal:
          metal += (RItem.value * item[0])
        else:
          RUserItem = getattr(RUser.Items[0], RItem.name)
          correctItems.append([RItem.name, item[0]])
      else:
        offer.decline()
        return False
    if offer.accept():
      correctItems.append(['metal', metal])
      for item in correctItems:
        itemValue = getattr(RUser.Items[0], item[0])
        itemValue += item[1]
        setattr(RUser.Items[0], item[0], itemValue)
        return True

  def Withdraw(self, offer, RUser):
    metal = 0
    correctItems = []
    for item in offer.itemsToGive:
      if item[1] in items:
        RItem = items[item[1]]
        if RItem.metal:
          metal += (RItem.value * item[0])
        else:
          RUserItem = getattr(RUser.Items[0], RItem.name)
          correctItems.append([RItem.name, item[0]])
      else:
        offer.decline()
        return False
    if offer.accept():
      correctItems.append(['metal', metal])
      for item in correctItems:
        itemValue = getattr(RUser.Items[0], item[0])
        itemValue -= item[1]
        setattr(RUser.Items[0], item[0], itemValue)
        return 2
    else:
      return 1

queue = {}
current = {}
class QueueHandler:
  def add(self, botID, steamID):
    queue[botID].append(steamID)
    if len(queue[botID]) == 1:
      jsonString = json.dumps(["hello",botID])
    else:
      jsonString = json.dumps(["queue", "position", len(queue[botID]) - 1])
    listeners[steamID].sendMessage(jsonString)

  def timeout(self, botID, steamID):
    current['withdraw'] = '';
    if steamID in listeners:
      listeners[steamID].sendClose()

  def remove(self, botID, steamID):
    if steamID in queue[botID]:
      queue[botID].remove(steamID)
    self.update(botID)

  def update(self, botID):
    for position, steamID in enumerate(queue[botID]):
      if position == 0:
        if current['withdraw'] != steamID:
          current['withdraw'] = steamID
          jsonString = json.dumps(["hello",botID])
          r = threading.Timer(60.0, self.timeout, [steamID])
          r.start()
      else:
        jsonString = json.dumps(["queue", "position", position])
      listeners[steamID].sendMessage(jsonString)

threads = []

listeners = {}
Bots = {}
for RBot in RBots:
  Bot = SteamWeb.Bot(
    RBot.id,
    RBot.name,
    {"login": RBot.steamLogin, "password": RBot.steamPassword, "id": RBot.steamID, "api": RBot.steamAPI, "trade": RBot.tradeLink},
    SteamWebCallback(RBot)
  )
  Bots[RBot.id] = Bot
  queue[RBot.id] = []
  current[RBot.id] = []

class BotServerProtocol(WebSocketServerProtocol):
  def onConnect(self, request):
    print("Client connecting: {0}".format(request.peer))

  def onOpen(self):
    print("WebSocket connection open.")
    if "127.0.0.1" in self.peer:
      print "Listen.js connected"
      for RBot in RBots:
        data = {
          "id": RBot.id,
          "name": RBot.name,
          "steamLogin": RBot.steamLogin,
          "steamPassword": RBot.steamPassword
        }
        jsonString = json.dumps(["bot", data]);
        self.sendMessage(jsonString)

  def onMessage(self, payload, isBinary):
    if not isBinary:
      message = payload.decode('utf8')
      message = json.loads(message)
      print message
      if message[0] == u"hello":
        steamID = int(message[2])
        self.RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
        listeners[steamID] = self
        if message[1] == u"withdraw":
          QueueHandler().add(self.RUser.bot, steamID)
        else:
          jsonString = json.dumps(["hello", self.RUser.bot])
          self.sendMessage(jsonString)
      if "127.0.0.1" in self.peer:
        if message[0] == u"tradeOffers":
          botID = message[1]
          Bot = Bots[botID]
          RBot = RBots[botID-1]
          threads.append(threading.Thread(target=OfferHandler, args=(Bot, RBot)))
          threads[-1].daemon = True
          threads[-1].start()
        elif message[0] == u"guardCode":
          RBot = RBots[message[1] - 1]
          data = {
            "id": RBot.id,
            "name": RBot.name,
            "steamLogin": RBot.steamLogin,
            "steamPassword": RBot.steamPassword
          }
          guardCode = Bots[RBot.id].Callback.steamGuard();
          jsonString = json.dumps(["bot", data, guardCode]);
          self.sendMessage(jsonString)

  def onClose(self, wasClean, code, reason):
    print("WebSocket connection closed: {0}".format(reason))
    leaverID = False
    for steamID, listener in listeners.items():
      if listener == self:
        leaverID = steamID
        break
    if leaverID:
      QueueHandler().remove(self.RUser.bot, leaverID)
      del listeners[leaverID]

import sys

from twisted.python import log
from twisted.internet import reactor

log.startLogging(sys.stdout)

factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
factory.protocol = BotServerProtocol

reactor.listenTCP(9000, factory)
reactor.run()