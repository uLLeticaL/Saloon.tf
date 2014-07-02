import sys
import re, time, json
import gmail
import database as db
import colorama as color
import threading
import SteamWeb

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

from twisted.python import log
log.startLogging(sys.stdout)

RBots = db.Session.query(db.Bots).all()
RItems = db.Session.query(db.Items).all()
items = {}
for RItem in RItems:
  classID = str(RItem.classID)
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

  def Trades(self):
    return self.OTrades(self)

  class OTrades(object):
    def __init__(self, Handler):
      self.Meta = Handler.Meta
      self.Bot = Handler.Bot
      self.Communicate = Handler.Communicate
      partners = {}
      self.Bot.Log("Trying to get offer information")
      # This one tends to timeout pretty often
      offers = self.Bot.Trade().GetOffers()
      self.Bot.Log("Got offer information")
      if offers is not False:
        if len(offers) > 0:
          accepted = False
          # Rework the dictionary to partner => offers format and
          for offerID in offers:
            offer = offers[offerID]
            steamID = offer.Partner.steamID
            if int(steamID) in Handler.Communicate.listeners:
              if steamID in partners:
                partners[steamID].append(offer)
              else:
                partners[steamID] = [offer]
            else:
              offer.decline()

          # Begin processing trades if they meet requirements (online)
          if len(partners) > 0:
            steamIDs = partners.keys()
            db.Session.commit()
            RUsers = db.Session.query(db.Users).filter(db.Users.steamID.in_(steamIDs)).all()
            for RUser in RUsers:
              for offer in partners[str(RUser.steamID)]:
                status = 0
                # Call offer handlers depending on the type of offer
                if self.offerType(offer) is "Deposit":
                  status = self.deposit(offer, RUser)
                elif self.offerType(offer) is "Withdrawal":
                  if RUser.steamID not in Handler.queue:
                    self.Bot.Log("User #" + RUser.steamID + " is not in the queue and his offer (" + str(offer.offerID) + ") will be declined.")
                    status = 3
                  else:
                    status = self.withdraw(offer, RUser)
                else:
                  offer.decline()
                  status = 2
                # Send error messages to the users
                if status == 0:
                  self.Communicate.send(["error"], RUser.steamID)
                elif status == 1:
                  accepted = True
                  self.Bot.Log("Accepted trade #" + str(offer.offerID) + " from " + RUser.name + ".")
                  self.Communicate.send(["accepted"], RUser.steamID)
                  self.Communicate.close(steamID)
                elif status == 2:
                  self.Communicate.send(["declined"], RUser.steamID)
              del partners[str(RUser.steamID)]

            # Decline offers made by not registered users
            for steamID in partners:
              self.Bot.Log("User with SteamID: " + str(steamID) + " isn't registered yet. Declining his offers.")
              for offer in partners[steamID]:
                offer.decline()
            # Commit session if any trade was accepted
            if accepted:
              db.Session.commit()

    def offerType(self, offer):
      if offer.itemsToReceive and not offer.itemsToGive:
        return "Deposit"
      elif offer.itemsToGive and not offer.itemsToReceive:
        return "Withdrawal"
      else:
        return False

    def deposit(self, offer, RUser):
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
          return 2
      if offer.accept():
        correctItems.append(['metal', metal])
        for item in correctItems:
          itemValue = getattr(RUser.Items[0], item[0])
          itemValue += item[1]
          setattr(RUser.Items[0], item[0], itemValue)
        return 1
      return 0

    def withdraw(self, offer, RUser):
      metal = 0
      correctItems = []
      for item in offer.itemsToGive:
        if item[1] in items:
          RItem = items[item[1]]
          if RItem.metal:
            metal += (RItem.value * item[0])
          else:
            RUserItem = getattr(RUser.Items[0], RItem.name)
            if RUserItem >= item[0]:
              correctItems.append([RItem.name, item[0]])
            else:
              offer.decline()
              return 2
        else:
          offer.decline()
          return 2

      if RUser.Items[0].metal < metal:
        offer.decline()
        return 2
      if offer.accept():
        correctItems.append(['metal', metal])
        for item in correctItems:
          itemValue = getattr(RUser.Items[0], item[0])
          itemValue -= item[1]
          setattr(RUser.Items[0], item[0], itemValue)
        return 1
      return 0

  def Queue(self):
    return self.OQueue(self)

  class OQueue(object):
    def __init__(self, Handler):
      self.Meta = Handler.Meta
      self.Bot = Handler.Bot
      self.Communicate = Handler.Communicate
      self.queue = Handler.queue
      self.current = Handler.current

    def add(self, steamID):
      self.queue.append(steamID)
      if len(self.queue) == 1:
        array = ["hello",self.Bot.id]
        r = threading.Timer(60.0, self.timeout, [steamID])
        r.start()
      else:
        array = ["queue", "position", len(self.queue) - 1]
      self.Communicate.send(array, steamID)

    def timeout(self, steamID):
      self.Communicate.close(steamID)

    def remove(self, steamID):
      if steamID in self.queue:
        print 1
        self.queue.remove(steamID)
      self.update()

    def update(self):
      for position, steamID in enumerate(self.queue):
        if position == 0:
          if self.current["withdraw"] != steamID:
            self.current["withdraw"] = steamID
            self.Communicate.send(["hello", self.Bot.id], steamID)
            r = threading.Timer(60.0, self.timeout, [steamID])
            r.start()
        else:
          self.Communicate.send(["queue", "position", position], steamID)

class OCommunicate(object):
  def __init__(self):
    self.listeners = {}
    self.listenjs = False
  def send(self, array, steamID):
    if steamID in self.listeners:
      self.listeners[steamID].sendMessage(json.dumps(array))
  def sendListenjs(self, array):
    if self.listenjs:
      self.listenjs.sendMessage(json.dumps(array))
  def add(self, user, steamID):
    self.listeners[steamID] = user
  def close(self, steamID):
    if steamID in self.listeners:
      self.listeners[steamID].sendClose()
  def remove(self, user):
    for steamID, listener in self.listeners.items():
      if listener == user:
        RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
        Handlers[RUser.bot].Queue().remove(steamID)
        del self.listeners[steamID]
  def log(self, handler, name, message):
    print color.Fore.YELLOW + color.Style.BRIGHT + "[" + handler + "] " + color.Fore.GREEN + "[" + name + "] " + color.Fore.RESET + color.Style.RESET_ALL + message

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
      if message[0] == u"hello":
        steamID = int(message[2])
        RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
        if RUser:
          Communicate.add(self, steamID)
          if message[1] == u"withdraw":
            Handlers[RUser.bot].Queue().add(steamID)
          else:
            Communicate.send(["hello", RUser.bot], steamID)
      if "127.0.0.1" in self.peer:
        if message[0] == u"log":
          Communicate.log("Listen.js", message[1], message[2])
        elif message[0] == u"tradeOffers":
          Handlers[message[1]].Trades()
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

from twisted.internet import reactor

factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
factory.protocol = BotServerProtocol

reactor.listenTCP(9000, factory)
reactor.run()