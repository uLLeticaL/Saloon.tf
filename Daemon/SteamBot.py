from mechanize import Browser, HTTPError, URLError
import time, json, threading, colorama as color
import urllib
from collections import defaultdict, Counter
from sqlalchemy import and_
import database as db
import SteamWeb

# Twisted's deffered module for non-blocking operations
from twisted.internet.threads import deferToThread
deferred = deferToThread.__get__

browser = Browser()
browser.set_handle_robots(False)
RBots = db.Session.query(db.Bots).all()

class Handler(object):
  def __init__(self, Meta, Communicate):
    self.running = True
    self.Meta = Meta
    self.Communicate = Communicate
    self.Bot = SteamWeb.Bot(
      self.Meta.id,
      self.Meta.name,
      {"login": self.Meta.steamLogin, "password": self.Meta.steamPassword, "id": self.Meta.steamID, "api": self.Meta.steamAPI, "trade": self.Meta.tradeLink},
      self.Callback()
    )
    self.checklist = {}
    self.Schema = Schema(self)

  def Callback(self):
    return self.OCallback(self)

  class OCallback(object):
    def __init__(self, Handler):
      self.Communicate = Handler.Communicate
      self.Meta = Handler.Meta

    def log(self, name, message):
      self.Communicate.log("SteamBot.py", self.Bot.name, message)

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
      self.Handler = Handler
      self.Bot = Handler.Bot
      self.Communicate = Handler.Communicate
      self.Schema = Handler.Schema
      self.Partner = self.Bot.Community().Friend(steamID)
      self.steamID = steamID
      self.userID = userID
      self.matchID = matchID
      self.teamID = teamID
      self.items = items
      self.checklist = Handler.checklist
      self.timeouted = False

      self.RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
      self.RBet = db.Session.query(db.Bets).filter(and_(db.Bets.user == userID, db.Bets.match == matchID)).first()
      self.increase = False
      if self.RBet:
        self.increase = True
        if self.RBet.team != teamID:
          self.Communicate.send(["bet", "error"], steamID)
          return False

      self.Communicate.send(["bet", "processing"], steamID)

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
        self.monitor(self)
      else:
        self.Communicate.send(["tradeOffer", False], self.steamID)

    @deferred
    def monitor(self):
      offer = self.Bot.Trade().Offer(self.offerID, self.Partner)
      r = threading.Timer(60.0, self.timeout, [offer])
      r.start()
      while not self.timeouted:
        offer.summary()
        if offer.state == 3 or offer.state == 8:
          r.cancel()
          self.process(offer)
          return True
        elif not offer.state == 2:
          self.Communicate.send(["accepted", False], self.steamID)
          return False
        elif not self.Handler.running:
          r.cancel()
          offer.cancel()
          break
        time.sleep(1)

    def process(self, offer):
      RBetsTotal = db.Session.query(db.BetsTotal).filter(and_(db.BetsTotal.match == self.matchID, db.BetsTotal.team ==self.teamID)).first()
      # Add self.RBet in case it's not an increase
      if not self.increase:
        self.RBet = db.Bets(user = self.userID, match = self.matchID, team = self.teamID, groups = [], items = [], value = 0)
        db.Session.add(self.RBet)
      
      # Convert PostgreSQL's multidimensional array to Counter dictionary
      totalGroups = defaultdict(Counter)
      for group in RBetsTotal.groups:
        totalGroups[group[0]][group[1]] = group[2]
      
      # Convert PostgreSQL's multidimensional array to dictionary
      usersGroups = defaultdict(Counter)
      for group in self.RBet.groups:
        usersGroups[group[0]][group[1]] = group[2]
      
      # Process new items information checking if items are really in the inventory
      betGroups = defaultdict(Counter)
      accepted = False
      inventory = self.Bot.Community().Inventory()
      itemsOrder = self.Schema.order(inventory.keys())
      itemsMeta = self.Schema.meta(inventory.keys())
      for orderedItem in itemsOrder:
        defindex = orderedItem["defindex"]
        quality = orderedItem["quality"]
        items = inventory[defindex]
        for id, item in items.items():
          if item["originID"] in self.checklist[self.steamID] and item["quality"] == quality:
            accepted = True
            self.checklist[self.steamID].remove(item["originID"])
            RBetsTotal.value += itemsMeta[defindex][quality].value
            self.RBet.value += itemsMeta[defindex][quality].value
            self.RBet.items.append(item["assetID"])
            usersGroups[defindex][quality] += 1
            totalGroups[defindex][quality] += 1
      if not accepted:
        return False

      # Merge betGroups with usersGroup and save result in database
      orderedGroups = []
      orderedItems = self.Schema.order(usersGroups.keys())
      for orderedItem in orderedItems:
        defindex = orderedItem["defindex"]
        quality = orderedItem["quality"]
        if quality in usersGroups[defindex]:
          orderedGroups.append([defindex, quality, usersGroups[defindex][quality]])
      self.RBet.groups = orderedGroups
      
      # Merge betGroups with totalGroups and save result in database
      orderedGroups = []
      orderedItems = self.Schema.order(totalGroups.keys())
      for orderedItem in orderedItems:
        defindex = orderedItem["defindex"]
        quality = orderedItem["quality"]
        if quality in totalGroups[defindex]:
          orderedGroups.append([defindex, quality, totalGroups[defindex][quality]])
      RBetsTotal.groups = orderedGroups
      
      db.Session.commit()
      self.Bot.browser.open("http://staging.saloon.tf/api/refreshsession")
      self.Communicate.send(["accepted", True], self.steamID)
      return True

    def timeout(self, offer):
      self.timeouted = True
      offer.cancel()
      self.Communicate.close(self.steamID)

  def inventory(self, steamID):
    RUser = db.Session.query(db.Users).filter(db.Users.steamID == steamID).first()
    if RUser:
      Partner = self.Bot.Community().Friend(steamID)
      Partner.token = RUser.token
      inventory = Partner.inventory()
      self.checklist[steamID] = []
      if inventory:
        response = []
        itemsOrder = self.Schema.order(inventory.keys())
        itemsMeta = self.Schema.meta(inventory.keys())
        for orderedItem in itemsOrder:
          defindex = orderedItem["defindex"]
          quality = orderedItem["quality"]
          itemsGroup = {
            "name": itemsMeta[defindex].values()[0].description,
            "defindex": defindex,
            "quality": quality,
            "value": itemsMeta[defindex][quality].value,
            "items": {}
          }
          items = inventory[defindex]
          for id, item in items.items():
            if item["quality"] == quality:
              if item["craftable"] and item["tradable"] and item["quality"] in itemsMeta[defindex]:
                self.checklist[steamID].append(item["originID"])
                itemsGroup["items"][id] = item
          if itemsGroup["items"]:
            response.append(itemsGroup)
        return response
    return False

class Schema(object):
  def __init__(self, Handler):
    self.Bot = Handler.Bot
    self.Meta = Handler.Meta
    self.load()

  def load(self):
    self.items = {}
    self.ordered = []
    RItems = db.Session.query(db.Items).order_by(db.Items.type, db.Items.quality, db.Items.value.desc()).all()
    for RItem in RItems:
      if RItem.defindex not in self.items:
        self.items[RItem.defindex] = {}
      self.items[RItem.defindex][RItem.quality] = RItem
      self.ordered.append({"defindex": RItem.defindex, "quality": RItem.quality})
    return self.items

  def update(self):
    itemSchema = self.Bot.API("IEconItems_440/GetSchema/v0001", {})
    itemSchema = itemSchema[u"result"][u"items"]
    itemPrices = self.backpackAPI("IGetPrices/v4", {})
    itemPrices = itemPrices[u"response"][u"items"]

    types = {
      143: 1,
      5021: 2,
      5002: 5,
      5001: 5,
      5000: 5,
    }

    currency = {}
    currency["metal"] = {
      "defindex": 5002,
      "updated": False,
      "value": 9
    }
    price = itemPrices[u"Random Craft Hat"][u"prices"][u"6"][u"Tradable"][u"Craftable"][0]
    currency["hat"] = {
      "defindex": -1,
      "updated": True,
      "value": round(price[u"value"] * currency["metal"]["value"])
    }
    price = itemPrices[u"Mann Co. Supply Crate Key"][u"prices"][u"6"][u"Tradable"][u"Craftable"][0]
    currency["keys"] = {
      "defindex": 5021,
      "updated": False,
      "value": round(price[u"value"] * currency["metal"]["value"])
    }
    if 5021 in self.items:
      currency["keys"]["updated"] = self.items[5021][6].timestamp > price[u"last_update"]
    price = itemPrices[u"Earbuds"][u"prices"][u"6"][u"Tradable"][u"Craftable"][0]
    currency["earbuds"] = {
      "defindex": 143,
      "updated": False,
      "value": round(price[u"value"] * currency["keys"]["value"])
    }
    if 143 in self.items:
      currency["earbuds"]["updated"] = self.items[143][6].timestamp > price[u"last_update"]

    prices = {}
    for name, item in itemPrices.items():
      if len(item[u"defindex"]) > 0:
        defindex = item[u"defindex"][0]
        try:
          for quality, price in item[u"prices"].items():
            quality = int(quality)
            if quality in [1,3,6]:
              price = price[u"Tradable"][u"Craftable"][0]
              value = 0.5 * round(2.0 * price[u"value"] * currency[price[u"currency"]]["value"])
              if value >= 1.0 and value <= currency["earbuds"]["value"]:
                if defindex in self.items and quality in self.items[defindex] and self.items[defindex][quality].timestamp <= price[u"last_update"] and not currency[price[u"currency"]]["updated"]:
                  continue
                if defindex not in prices:
                  prices[defindex] = {}
                prices[defindex][quality] = {
                  "name": name,
                  "value": int(value),
                  "updated": price[u"last_update"]
                }
        except KeyError:
          pass

    for item in itemSchema:
      if item[u"defindex"] in prices:
        if item[u"defindex"] in types:
          kind = types[item[u"defindex"]]
        elif u"craft_class" in item and item[u"craft_class"] == u"hat":
          kind = 3
        elif u"tool" in item and item[u"tool"][u"type"] == u"paint_can":
          kind = 4
        else:
          continue
        if item[u"defindex"] in prices:
          for quality, price in prices[item[u"defindex"]].items():
            if item[u"defindex"] in self.items:
              if quality in self.items[item[u"defindex"]]:
                self.Bot.Log(price["name"] + " updated from " + str(RItem.value) + " to " + str(price["value"]))
                RItem.value = price["value"]
                RItem.timestamp = price["updated"]
                continue
            else:
              imagePath = "../Website/website/public/images/items/" + str(item[u"defindex"]) + ".png"
              image = browser.open(item[u"image_url"]).read()
              imageFile = open(imagePath, 'wb')
              imageFile.write(image)
              imageFile.close()
            RItem = db.Items(description = price["name"], value = price["value"], defindex = item[u"defindex"], type = kind, quality = quality, timestamp = price["updated"])
            db.Session.add(RItem)
            self.Bot.Log(price["name"] + " added.")
    db.Session.commit()
    self.load()
    browser.open("http://staging.saloon.tf/api/refreshsession")

  def order(self, items):
    order = []
    for item in self.ordered:
      if item["defindex"] in items and item not in order:
        order.append(item)
    return order

  def meta(self, items):
    response = {}
    for defindex in items:
      if defindex in self.items:
        response[defindex] = self.items[defindex]
    return response

  def backpackAPI(self, action, parameters):
    parameters["key"] = self.Meta.backpackAPI
    parameters["compress"] = 1
    data = urllib.urlencode(parameters)
    for i in range(3):
      try:
        response = self.Bot.browser.open("http://backpack.tf/api/" + action + "/?" + data)
        response = json.loads(response.read())
        return response
      except (HTTPError, URLError) as error:
        continue
    return False