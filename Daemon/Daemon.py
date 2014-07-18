from mechanize import Browser, HTTPError, URLError
import sys, re, time, json, gmail, colorama as color
from sqlalchemy.dialects.postgresql import array
from sqlalchemy import and_
from SteamBot import Handler
import database as db

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

from twisted.internet import reactor
from twisted.python import log
log.startLogging(sys.stdout)

RBots = db.Session.query(db.Bots).all()

class OCommunicate(object):
  def __init__(self):
    self.listeners = {}
    self.listenjs = False

  def send(self, array, steamID):
    if steamID in self.listeners:
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

def shutdown():
  Communicate.log("Daemon.py", "Communicate", "Trying to shutdown Handlers")
  for Handler in Handlers.values():
    Handler.running = False

class ServerProtocol(WebSocketServerProtocol):
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
            Communicate.send(["inventory", Handler.inventory(steamID)], steamID)
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
          Communicate.send(["inventory", Handler.inventory(steamID)], steamID)
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
factory.protocol = ServerProtocol

reactor.listenTCP(9000, factory)
reactor.addSystemEventTrigger('during', 'shutdown', shutdown)
reactor.run()