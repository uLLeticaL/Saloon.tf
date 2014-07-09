import sys
import re, time, json
import gmail
import database as db
import colorama as color
import threading
import SteamWeb

from mechanize import Browser, HTTPError, URLError

from sqlalchemy import and_

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

from twisted.internet import reactor

from twisted.internet.threads import deferToThread
deferred = deferToThread.__get__

from twisted.python import log
log.startLogging(sys.stdout)

RBots = db.Session.query(db.Bots).all()
RItems = db.Session.query(db.Items).all()
items = {}
for RItem in RItems:
  classID = RItem.classID
  items[classID] = RItem

class Handler(object):
  def __init__(self, Meta, Communicate):
    self.Meta = Meta
    self.Communicate = Communicate
    self.Bot = SteamWeb.Bot(
      self.Meta.id,
      self.Meta.name,
      {"login": self.Meta.steamLogin, "password": self.Meta.steamPassword, "id": self.Meta.steamID, "api": self.Meta.steamAPI, "trade": self.Meta.tradeLink},
      self.Callback()
    )
    self.queue = []
    self.current = {"withdraw":""}

  def Callback(self):
    return self.OCallback(self)

  class OCallback(object):
    def __init__(self, Handler):
      self.Communicate = Handler.Communicate
      self.Meta = Handler.Meta

    def Log(self, name, message):
      self.Communicate.log("Crunch.py", self.Bot.name, message)

    def steamGuard(self):
      # Manual authentication
      if self.Meta.emailPassword is None:
        while True:
          self.log("GuardCode sent to " + self.Meta.emailAddress)
          guardCode = raw_input(color.Fore.BLUE + color.Style.BRIGHT + "[" + self.Bot.name + "] " + color.Fore.RESET + color.Style.RESET_ALL + "GuardCode: ")
          return guardCode
      else:
        g = gmail.login(self.Meta.emailAddress, self.Meta.emailPassword)
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
        self.log(Bot.name, "GuardCode sent to " + self.Meta.emailAddress + ". You'll have to manually enter the code.")
        guardCode = raw_input(color.Fore.BLUE + color.Style.BRIGHT + "[" + self.Bot.name + "] " + color.Fore.RESET + color.Style.RESET_ALL + "GuardCode: ")
        return guardCode

    def captchaCode(self, gid):
      # "Never give up on your goals, stay focused on your own"
      self.log(Bot.name, "Captcha needed. Saving it to the " + captchaPath)
      captchaPath = "captchas/" + self.Meta.name + "-" + response[u"captcha_gid"] + ".png"
      captcha = self.Bot.browser.open("https://steamcommunity.com/public/captcha.php?gid=" + gid).read()
      captchaFile = open(captchaPath, 'wb')
      captchaFile.write(captcha)
      captchaFile.close()
      captchaCode = raw_input(color.Fore.BLUE + color.Style.BRIGHT + "[" + self.Bot.name + "] " + color.Fore.RESET + color.Style.RESET_ALL + "Captcha: ")
      return captchaCode

  def Bet(self, steamID, userID, matchID, teamID, items):
    return self.OBet(self, steamID, userID, matchID, teamID, items)

  class OBet(object):
    def __init__(self, Handler, steamID, userID, matchID, teamID, items):
      self.Bot = Handler.Bot
      self.Communicate = Handler.Communicate
      self.Partner = self.Bot.Community().Friend(steamID)
      self.steamID = steamID
      self.userID = userID
      self.matchID = matchID
      self.teamID = teamID
      self.items = items
      self.timeouted = False

      self.RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
      self.RBet = db.Session.query(db.Bets).filter(and_(db.Bets.user == userID, db.Bets.match == matchID)).first()
      if not self.RBet or (self.RBet and self.RBet.team == teamID):
        Communicate.send(["bet", "processing"], steamID)

        self.Partner.token = self.RUser.token
        itemsToReceive = []
        for assetID in self.items:
          itemsToReceive.append({
            "appid": 440,
            "contextid": 2,
            "amount": 1,
            "assetid": str(assetID)
          })

        self.offerID = self.Bot.Trade().MakeOffer(self.Partner, [], itemsToReceive, "Thanks for betting with Saloon.tf!")
        if self.offerID:
          self.Communicate.send(["tradeOffer", self.offerID], self.steamID)
          self.monitorOffer(self)
        else:
          self.Communicate.send(["tradeOffer", False], self.steamID)
      else:
        Communicate.send(["bet", "error"], steamID)

    @deferred
    def monitorOffer(self):
      r = threading.Timer(120.0, self.timeout)
      r.start()
      while not self.timeouted:
        offer = self.Bot.Trade().Offer(self.offerID, self.Partner)
        if offer.state == 3:
          correctItems = {u"metal": 0}
          for item in offer.itemsToReceive:
            if item["classid"] in items:
              RItem = items[item["classid"]]
              if RItem.metal:
                correctItems[u"metal"] += RItem.value * item["amount"]
              else:
                if RItem.name in correctItems:
                  correctItems[RItem.name] += item["amount"]
                else:
                  correctItems[RItem.name] = item["amount"]
            else:
              offer.decline()
              self.Communicate.send(["accepted", False], self.steamID)
              return False

          if self.RBet:
            for item in correctItems:
              setattr(self.RBet, item, getattr(self.RBet, item) + correctItems[item])
          else:
            RBetDict = dict(correctItems.items() + [("user", self.userID), ("match", self.matchID), ("team", self.teamID)])
            RBet = db.Bets(**RBetDict)
            db.Session.add(RBet)

          RBetsTotal = db.Session.query(db.BetsTotal).filter(and_(db.BetsTotal.match == self.matchID, db.BetsTotal.team == self.teamID)).first()
          for item in correctItems:
            setattr(RBetsTotal, item, getattr(RBetsTotal, item) + correctItems[item])
          db.Session.commit()

          Browser().open("http://saloon.tf/api/refreshsession")
          self.Communicate.send(["accepted", True], self.steamID)
          return True
        elif offer.state == 4 or offer.state == 7:
          self.Communicate.send(["accepted", False], self.steamID)
          return False
        time.sleep(1)

    def timeout(self):
      self.timeouted = True
      self.Communicate.close(self.steamID)

  def GetInventory(self, steamID):
    Partner = self.Bot.Community().Friend(steamID)
    RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
    Partner.token = RUser.token
    inventory = Partner.inventory()
    if inventory[0]:
      response = {}
      for classID in inventory[1]:
        RItem = db.Session.query(db.Items).filter(db.Items.classID == classID).first()
        if RItem:
          response[RItem.name] = inventory[1][classID][3]
      return response
    return False

class OCommunicate(object):
  def __init__(self):
    self.listeners = {}
    self.listenjs = False
  def send(self, array, steamID):
    if steamID in self.listeners:
      print self.listeners[steamID]
      self.listeners[steamID].sendMessage(json.dumps(array))
      return json.dumps(array)

  def sendListenjs(self, array):
    if self.listenjs:
      self.listenjs.sendMessage(json.dumps(array))

  def add(self, user, steamID):
    self.listeners[steamID] = user

  def close(self, steamID):
    if steamID in self.listeners:
      self.listeners[steamID].sendClose()

  def remove(self, user):
    steamID = self.getSteamID(user)
    if steamID:
      RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
      del self.listeners[steamID]

  def log(self, handler, name, message):
    print color.Fore.YELLOW + color.Style.BRIGHT + "[" + handler + "] " + color.Fore.GREEN + "[" + name + "] " + color.Fore.RESET + color.Style.RESET_ALL + message

  def getSteamID(self, user):
    for steamID, listener in self.listeners.items():
      if listener == user:
        return steamID
    return False

Communicate = OCommunicate()
Handlers = {}
for RBot in RBots:
  Handlers[RBot.id] = Handler(RBot, Communicate)

class BotServerProtocol(WebSocketServerProtocol):
  def onConnect(self, request):
    print("Client connecting: {0}".format(request.peer))

  def onOpen(self):
    print("WebSocket connection open.")
    if "127.0.0.1" in self.peer:
      print "Listen.js connected"
      Communicate.listenjs = self
      for RBot in RBots:
        data = {
          "id": RBot.id,
          "name": RBot.name,
          "steamLogin": RBot.steamLogin,
          "steamPassword": RBot.steamPassword
        }
        self.sendMessage(json.dumps(["bot", data]))

  def onMessage(self, payload, isBinary):
    if not isBinary:
      message = payload.decode('utf8')
      message = json.loads(message)
      print message
      if message[0] == u"hello":
        steamID = int(message[1])
        RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
        if RUser:
          Handler = Handlers[RUser.bot]
          Communicate.add(self, steamID)
          if RUser.token:
            Communicate.send(["inventory", Handler.GetInventory(steamID)], steamID)
          else:
            Communicate.send(["tradeLink", "new"], steamID)
      elif message[0] == u"tradeLink":
        steamID = Communicate.getSteamID(self)
        match = re.match(u"http:\/\/steamcommunity\.com\/tradeoffer\/new\/\?partner=[0-9]+&token=([a-zA-Z0-9]+)", message[1])
        if match:
          RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
          RUser.token = match.group(1)
          db.Session.commit()
          Handler = Handlers[RUser.bot]
          Communicate.send(["inventory", Handler.GetInventory(steamID)], steamID)
        else:
          Communicate.send(["tradeLink", "wrong"], steamID)
      elif message[0] == u"bet":
        steamID = Communicate.getSteamID(self)
        if steamID:
          RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
          if RUser:
            Handler = Handlers[RUser.bot]
            Handler.Bet(steamID, RUser.id, message[1], message[2], message[3])
      if "127.0.0.1" in self.peer:
        if message[0] == u"log":
          Communicate.log("Listen.js", message[1], message[2])
        elif message[0] == u"guardCode":
          Handler = Handlers[message[1]]
          data = {
            "id": Handler.Meta.id,
            "name": Handler.Meta.name,
            "steamLogin": Handler.Meta.steamLogin,
            "steamPassword": Handler.Meta.steamPassword
          }
          guardCode = Handler.WebCallback.steamGuard()
          self.sendMessage(json.dumps(["bot", data, guardCode]))

  def onClose(self, wasClean, code, reason):
    print("WebSocket connection closed: {0}".format(reason))
    Communicate.remove(self)

factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
factory.protocol = BotServerProtocol

reactor.listenTCP(9000, factory)
reactor.run()