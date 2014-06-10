import time, json
import settings, database as db
import threading
import SteamWeb

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

bot = SteamWeb.Bot(settings.bots[0])
trade = bot.Trade()
items = {}
RItems = db.Session.query(db.Items).all()
for RItem in RItems:
  classID = str(RItem.classID)
  items[classID] = RItem
listeners = {}
threads = []
queue = []

current = {
  'withdraw': '',
  'deposit': ''
}

class TradesHandler(threading.Thread):
  def run(self):
    while True:
      partners = {}
      offers = trade.GetOffers()
      if len(offers) > 0:
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
            metal = 0
            correctItems = []
            if offer.itemsToReceive and not offer.itemsToGive:
              success = OfferHandler(offer, RUser).Deposit()
            elif offer.itemsToGive and not offer.itemsToReceive:
              if RUser.steamID not in queue:
                success = False
              else:
                success = OfferHandler(offer, RUser).Withdraw()
            else:
              success = False

            if success:
              print offer.accept()
              bot.Log("Accepted trade #" + str(offer.offerID) + " from " + RUser.name + ".")
              if RUser.steamID in listeners:
                jsonString = json.dumps(["accepted"])
                listeners[RUser.steamID].sendMessage(jsonString)
              if RUser.steamID in queue:
                QueueHandler().timeout(steamID)
            else:
              offer.decline()
              bot.Log("Trade #" + str(offer.offerID) + " had invalid items. Declining.")
              if RUser.steamID in listeners:
                jsonString = json.dumps(["declined"])
                listeners[RUser.steamID].sendMessage(jsonString)
          del partners[str(RUser.steamID)]

        for steamID in partners:
          bot.Log("User with SteamID: " + str(steamID) + " isn't registered yet. Declining his offers.")
          for offer in partners[steamID]:
            offer.decline()
      db.Session.commit()
      time.sleep(3)

class OfferHandler(object):
  def __init__(self, offer, RUser):
    self.RUser = RUser
    self.offer = offer

  def Deposit(self):
    metal = 0
    correctItems = []
    for item in self.offer.itemsToReceive:
      if item[1] in items:
        RItem = items[item[1]]
        if RItem.metal:
          metal += (RItem.value * item[0])
        else:
          RUserItem = getattr(self.RUser.Items[0], RItem.name)
          correctItems.append([RUserItem, item[0]])
      else:
        return False
    correctItems.append(['metal', metal])
    for item in correctItems:
      itemValue = getattr(self.RUser.Items[0], item[0])
      itemValue += item[1]
      setattr(self.RUser.Items[0], item[0], itemValue)
      return True

  def Withdraw(self):
    metal = 0
    correctItems = []
    for item in self.offer.itemsToGive:
      if item[1] in items:
        RItem = items[item[1]]
        if RItem.metal:
          metal += (RItem.value * item[0])
        else:
          RUserItem = getattr(self.RUser.Items[0], RItem.name)
          correctItems.append([RUserItem, item[0]])
      else:
        return False
    correctItems.append(['metal', metal])
    for item in correctItems:
      itemValue = getattr(self.RUser.Items[0], item[0])
      itemValue -= item[1]
      setattr(self.RUser.Items[0], item[0], itemValue)
      return True

class QueueHandler:
  def add(self, steamID):
    queue.append(steamID)
    if len(queue) == 1:
      jsonString = json.dumps(["hello",bot.Meta.id])
      r = threading.Timer(60.0, self.timeout, [steamID])
      r.daemon = True
      r.start()
    else:
      jsonString = json.dumps(["queue", "position", len(queue) - 1])
    listeners[steamID].sendMessage(jsonString)

  def timeout(self, steamID):
    current['withdraw'] = '';
    if steamID in listeners:
      listeners[steamID].sendClose()

  def remove(self, steamID):
    current['withdraw'] = '';
    if steamID in queue:
      queue.remove(steamID)
    self.update()

  def update(self):
    print current
    print queue
    for position, steamID in enumerate(queue):
      if position == 0:
        if current['withdraw'] != steamID:
          current['withdraw'] = steamID
          jsonString = json.dumps(["hello",bot.Meta.id])
          r = threading.Timer(60.0, self.timeout, [steamID])
          r.start()
      else:
        jsonString = json.dumps(["queue", "position", position])
      listeners[steamID].sendMessage(jsonString)

class BotServerProtocol(WebSocketServerProtocol):
  def onConnect(self, request):
    print("Client connecting: {0}".format(request.peer))

  def onOpen(self):
    print("WebSocket connection open.")

  def onMessage(self, payload, isBinary):
    if not isBinary:
      message = payload.decode('utf8')
      message = json.loads(message)
      print message
      if message[0] == u"hello":
        steamID = int(message[2])
        listeners[steamID] = self
        print message[1]
        if message[1] == u"withdraw":
          QueueHandler().add(steamID)
        else:
          jsonString = json.dumps(["hello",bot.Meta.id])
          self.sendMessage(jsonString)

  def onClose(self, wasClean, code, reason):
    print("WebSocket connection closed: {0}".format(reason))
    leaverID = False
    for steamID, listener in listeners.items():
      if listener == self:
        leaverID = steamID
        break
    if leaverID:
      QueueHandler().remove(leaverID)
      del listeners[leaverID]

threads.append(TradesHandler())
threads[-1].daemon = True
threads[-1].start()

import sys

from twisted.python import log
from twisted.internet import reactor

log.startLogging(sys.stdout)

factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
factory.protocol = BotServerProtocol

reactor.listenTCP(9000, factory)
reactor.run()