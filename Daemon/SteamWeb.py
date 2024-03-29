from mechanize import Browser, HTTPError, URLError
import re, os, time, json, base64, colorama as color
import urllib, cookielib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

class Bot(object):
  def __init__(self, botID, name, steam, Callback):
    self.id = botID
    self.name = name
    self.steam = steam

    self.Callback = Callback
    self.Callback.Bot = self

    self.cookiejar = cookielib.LWPCookieJar()
    self.cookiefile = "cookies/" + self.steam["login"]
    if os.path.isfile(self.cookiefile):
      self.cookiejar.load(self.cookiefile)

    self.browser = Browser()
    self.browser.set_handle_robots(False)
    self.browser.set_cookiejar(self.cookiejar)

    self.Authenticate()

  def Log(self, message):
    self.Callback.log(self.name, message)

  def Community(self):
    # Pass Bot to the O objects.
    return self.OCommunity(self)

  def Trade(self):
    # Pass Bot to the O objects.
    return self.OTrade(self)

  def Authenticate(self):
    # Pass Bot to the O objects.
    return self.OAuth(self)

  class OAuth(object):
    def __init__(self, bot):
      self.Bot = bot
      self.signIn()

    def signIn(self, guardNeeded = False, steamID = "", encrypted = "", captchaNeeded = False, captchaGid = "", captchaCode = ""):
      if guardNeeded:
        self.Bot.Log("SteamGuard code needed")
      else:
        self.Bot.Log("Encrypting password")
        encrypted = self.encryptPassword(self.Bot.steam["login"], self.Bot.steam["password"].encode("ascii","ignore"))
        self.Bot.Log("Logging in")

      parameters = {
        'username': self.Bot.steam["login"],
        'password': encrypted["password"],
        'emailauth': "",
        'loginfriendlyname': "",
        'captchegid': "",
        'emailsteamid': "",
        'rsatimestamp': encrypted["timestamp"],
        'remember_login': "true",
        'donotcache': int(time.time())
      }

      if guardNeeded:
        guardCode = self.Bot.Callback.steamGuard()
        parameters["emailauth"] = guardCode
        parameters["loginfriendlyname"] = "Saloon.TF"
        parameters["emailsteamid"] = steamID
        self.Bot.Log("Logging in again with SteamGuard code")
      if captchaNeeded:
        parameters["captchagid"] = captchaGid
        parameters["captcha_text"] = captchaCode

      data = urllib.urlencode(parameters)
      response = self.Bot.browser.open("https://steamcommunity.com/login/dologin/", data)
      response = json.loads(response.read())
      if response[u"success"]:
        self.Bot.cookiejar.save(self.Bot.cookiefile)
        self.Bot.sessionid = self.getSessionId()
        self.Bot.Log("Logged in successfully")
        return True
      elif response[u"message"] == u"SteamGuard":
        # Try to log in again using SteamGuard code
        self.signIn(guardNeeded = True, steamID = response[u"emailsteamid"], encrypted = encrypted)
      elif response[u"message"] == u"Error verifying humanity":
        captchaCode = self.Bot.Callback.captchaCode(response[u"captcha_gid"])
        self.signIn(captchaNeeded = True, captchaGid = response[u"captcha_gid"], captchaCode = captchaCode)
      else:
        self.Bot.Log("Something went wrong. Message: " + response[u"message"])
        return False

    def encryptPassword(self, login, password):
      # Get RSA key from Steam
      parameters = {
        'username' : login
      }
      data = urllib.urlencode(parameters)
      response = self.Bot.browser.open("https://store.steampowered.com/login/getrsakey/", data)
      response = json.loads(response.read())
      # Generate public key from modulus and exponent
      implementation = RSA.RSAImplementation(use_fast_math = False)
      modulus = long(response["publickey_mod"], 16)
      exponent = long(response["publickey_exp"], 16)
      rsaKey = implementation.construct((modulus, exponent))
      rsaKey = PKCS1_v1_5.new(rsaKey) 
      encryptedPassword = rsaKey.encrypt(password)
      return {'password': base64.b64encode(encryptedPassword), 'timestamp': response["timestamp"]}
          
    def getSessionId(self):
      response = self.Bot.browser.open("http://steamcommunity.com/profiles/GoHomeValveYoureDrunk")
      sessionId = re.findall(r'g_sessionID = "(.*?)";', response.read())[0]
      return sessionId

  class OCommunity(object):
    def __init__(self, bot):
      self.Bot = bot

    def GetFriends(self, prefetch = False):
      parameters = {'relationship': 'friend', 'steamid': self.Bot.steam["id"]}
      response = self.Bot.API("ISteamUser/GetFriendList/v0001", parameters)
      friends = []
      if prefetch:
        steamIDs = []
        blocks = []
        count = 0
      for friend in response[u"friendslist"][u"friends"]:
        steamID = friend[u"steamid"].encode('ascii', 'ignore')
        friends.append(self.Friend(steamID, prefetch))
        if prefetch:
          steamIDs.append(steamID)
          count += 1
          if count == 100:
            blocks.append(",".join(steamIDs))
            steamIDs = []
            count = 0
      if prefetch:
        blocks.append(",".join(steamIDs))
        count = 0
        for block in blocks:
          parameters = {'relationship': 'friend', 'steamids': block}
          response = self.Bot.API("ISteamUser/GetPlayerSummaries/v0002", parameters)
          response = response[u"response"][u"players"]
          if count + 100 > len(friends):
            r = range(0, len(friends) % 100)
          else:
            r = range(0,100)
          for i in r:
            friends[count].name = response[i][u"personaname"]
            friends[count].state = response[i][u"personastate"]
            friends[count].avatar = response[i][u"avatarfull"]
            friends[count].public = True if response[i][u"communityvisibilitystate"] is 3 else False
            count += 1
      return friends

    def Inventory(self):
      return self.OFriend(self.Bot, self.Bot.steam["id"], False).inventory()

    def Friend(self, steamID, prefetch = False):
      return self.OFriend(self.Bot, steamID, prefetch)

    class OFriend:
      def __init__(self, bot, steamID, prefetch):
        self.steamID = steamID
        self.SID = SID(communityID = steamID)
        self.Bot = bot
        self.token = False
        if not prefetch:
          self.summary()

      def add(self):
        parameters = {
          'steamid': str(self.steamID),
          'accept_invite': 0
        }
        response = self.Bot.Ajax('AddFriendAjax', parameters)
        if response:
          self.Bot.Log("Sent friend request to " + str(self.steamID))
          return True
        else:
          self.Bot.Log("Couldn't add " + str(self.steamID) + " to the friends list.")
          return False

      def accept(self):
        parameters = {
          'steamid': self.steamID,
          'accept_invite': 1
        }
        response = self.Bot.Ajax('AddFriendAjax', parameters)
        if response:
          self.Bot.Log("Accepted friend request from " + str(self.steamID))
          return True
        else:
          self.Bot.Log("Couldn't add " + str(self.steamID) + " to the friends list.")
          return False

      def remove(self):
        parameters = {
          'steamid': self.steamID
        }
        response = self.Bot.Ajax('RemoveFriendAjax', parameters)
        if response:
          self.Bot.Log("Removed " + str(self.steamID) + " from the friends list.")
          return True
        else:
          self.Bot.Log("Couldn't remove " + str(self.steamID) + " from the friends list.")
          return False
      
      def inventory(self, appID = 440, contextID = 2):
        items = {}
        parameters = {'steamid': self.steamID}
        inventory = self.Bot.API("IEconItems_440/GetPlayerItems/v0001", parameters)
        if inventory:
          for item in inventory[u"result"][u"items"]:
            if item[u"defindex"] not in items:
              items[item[u"defindex"]] = {}
            items[item[u"defindex"]][item[u"id"]] = {
              "assetID": item[u"id"],
              "originID": item[u"original_id"],
              "level": item[u"level"],
              "quality": item[u"quality"],
              "origin": item[u"origin"],
              "tradable": not u"flag_cannot_trade" in item,
              "craftable": not u"flag_cannot_craft" in item
            }
          return items
        self.Bot.Log("Couldn't load inventory.")
        return False

      def summary(self):
        parameters = {'steamids': self.steamID}
        response = self.Bot.API("ISteamUser/GetPlayerSummaries/v0002", parameters)
        response = response[u"response"][u"players"][0]
        self.name = response[u"personaname"]
        self.state = response[u"personastate"]
        self.avatar = response[u"avatarfull"]
        self.public = True if response[u"communityvisibilitystate"] is 3 else False

  class OTrade(object):
    def __init__(self, bot):
      self.Bot = bot   

    def sendOffer(self, Partner, itemsToGive, itemsToReceive, message):
      createParams = {}
      parameters = {"partner": str(Partner.SID.toAccount())}
      if Partner.token:
        parameters["token"] = Partner.token
        createParams["trade_offer_access_token"] = Partner.token
      data = urllib.urlencode(parameters)
      self.Bot.browser.addheaders = [('Referer', "https://steamcommunity.com/tradeoffer/new/?" + data)]

      offerParams = {
        "newversion": True,
        "version": 4,
        "me": {
          "assets": itemsToGive,
          "currency": [],
          "ready": False
        },
        "them": {
          "assets": itemsToReceive,
          "currency": [],
          "ready": False
        }
      }

      parameters = {
        'partner': str(Partner.steamID).encode("utf-8"),
        'sessionid': self.Bot.sessionid.encode("utf-8"),
        'tradeoffermessage': message,
        'json_tradeoffer': json.dumps(offerParams),
        'trade_offer_create_params': json.dumps(createParams)
      }
      data = urllib.urlencode(parameters)
      for i in range(0,3):
        requestTime = int(round(time.time() * 1000))
        try:
          response = self.Bot.browser.open("https://steamcommunity.com/tradeoffer/new/send", data, timeout = 5.0)
          response = json.loads(response.read())
          return int(response["tradeofferid"])
        except (HTTPError, URLError) as error:
          parameters = {"get_sent_offers": 1}
          response = self.Bot.API("IEconService/GetTradeOffers/v0001", parameters)
          print response
          offers = response[u"response"][u"trade_offers_sent"]
          for offer in offers:
            if offer[u"time_created"] >= requestTime:
              if offer[u"accountid_other"] == Partner.SID.toAccount():
                return int(offer["tradeofferid"])
              else:
                continue
            else:
              break
          continue
      self.Bot.Log("Couldn't send tradeoffer.")
      return False

    def GetOffers(self, offerType = "received", offerState = 2, active = True):
      parameters = {
        'active_only': int(active),
        'time_historical_cutoff': int(time.time())
      }
      if offerType == "sent":
        parameters["get_sent_offers"] = 1
      else:
        parameters["get_received_offers"] = 1

      offersList = []
      response = self.Bot.API("IEconService/GetTradeOffers/v0001", parameters)
      if response:
        response = response[u"response"]
        if offerType == "sent":
          if u"trade_offers_sent" in response:
            offersList = response[u"trade_offers_sent"]
          else:
            offersList = []
        else:
          if u"trade_offers_received" in response:
            offersList = response[u"trade_offers_received"]
          else:
            offersList = []

        offers = {}
        for offer in offersList:
          offerID = int(offer[u"tradeofferid"])
          if offer[u"trade_offer_state"] == offerState:
            steamID = SID(accountID = offer[u"accountid_other"]).toCommunity()
            Partner = self.Bot.Community().Friend(steamID)
            offer = self.Offer(offerID, Partner)
            offers[offerID] = offer
        return offers
      else:
        return False

    def Offer(self, offerID, Partner = False):
      return self.OOffer(self.Bot, offerID, Partner)

    class OOffer:
      def __init__(self, bot, offerID, Partner = False):
        self.offerID = offerID
        self.Partner = Partner
        self.Bot = bot
        self.itemsToReceive = False
        self.itemsToGive = False
        self.summary()

      def accept(self):
        self.Bot.browser.addheaders = [('Referer', "https://steamcommunity.com/tradeoffer/" + str(self.offerID))]
        parameters = {
          'partner': self.Partner.steamID.encode("utf-8"),
          'tradeofferid': str(self.offerID).encode("utf-8"),
          'sessionid': self.Bot.sessionid.encode("utf-8")
        }
        data = urllib.urlencode(parameters)
        for i in range(0,3):
          try:
            response = self.Bot.browser.open("https://steamcommunity.com/tradeoffer/" + str(self.offerID) + "/accept", data, timeout = 5.0)
          except (HTTPError, URLError) as error:
            continue
          self.Bot.Log("Accepted #" + str(self.offerID) + " offer.")
          return True
        self.Bot.Log("Couldn't accept #" + str(self.offerID) + " offer. " + str(error.code) + " ERROR.")
        return False

      def decline(self):
        parameters = {
          'tradeofferid': str(self.offerID)
        }
        response = self.Bot.API("IEconService/DeclineTradeOffer/v1", parameters)
        if response:
          self.Bot.Log("Declined #" + str(self.offerID) + " offer.")
          return True
        else:
          self.Bot.Log("Couldn't decline #" + str(self.offerID) + " offer.")
          return False

      def cancel(self):
        parameters = {
          'tradeofferid': str(self.offerID)
        }
        response = self.Bot.API("IEconService/CancelTradeOffer/v1", parameters)
        if response:
          self.Bot.Log("Canceled #" + str(self.offerID) + " offer.")
          return True
        else:
          self.Bot.Log("Couldn't cancel #" + str(self.offerID) + " offer.")
          return False

      def summary(self):
        parameters = {'tradeofferid': str(self.offerID)}
        response = self.Bot.API("IEconService/GetTradeOffer/v0001", parameters)
        if response:
          response = response[u"response"]
          offer = response[u"offer"]
          self.state = offer[u"trade_offer_state"]
          self.message = offer[u"message"]
          self.expirationTime = offer[u"expiration_time"]
          if not self.itemsToReceive:
            descriptions = {}
            if u"descriptions" in response:
              for item in response[u"descriptions"]:
                descriptions[item["classid"] + "_" + item["instanceid"]] = item
            self.itemsToReceive = {}
            if u"items_to_receive" in offer:
              for item in offer[u"items_to_receive"]:
                classID = int(item[u"classid"])
                assetID = int(item[u"assetid"])
                if not classID in self.itemsToReceive:
                  self.itemsToReceive[classID] = {
                    "classID": classID,
                    "appid": int(item[u"appid"]),
                    "contextid": int(item[u"contextid"]),
                    "items": {}
                  }
                self.itemsToReceive[classID]["items"][assetID] = {}
                if descriptions:
                  description = descriptions[item["classid"] + "_" + item["instanceid"]]
                  self.itemsToReceive[classID]["name"] = description[u"name"]
                  self.itemsToReceive[classID]["type"] = description[u"type"]
                  self.itemsToReceive[classID]["items"][assetID] = {
                    "craftable": not (u"descriptions" in description and "( Not Usable in Crafting )" in [attribute["value"] for attribute in description[u"descriptions"]]),
                    "tradable": description[u"tradable"],
                    "background_color": description[u"background_color"],
                    "name_color": description[u"name_color"]
                  }

            self.itemsToGive = {}
            if u"items_to_give" in offer:
              for item in offer[u"items_to_receive"]:
                classID = int(item[u"classid"])
                assetID = int(item[u"assetid"])

                if not classID in self.itemsToGive:
                  self.itemsToGive[classID] = {
                    "classid": classID,
                    "assetid": int(item[u"assetid"]),
                    "appid": int(item[u"appid"]),
                    "contextid": int(item[u"contextid"]),
                    "items": {}
                  }
                self.itemsToGive[classID]["items"][assetID] = {}
                if descriptions:
                  description = descriptions[item["classid"] + "_" + item["instanceid"]]
                  self.itemsToGive[classID]["name"] = description[u"name"]
                  self.itemsToGive[classID]["type"] = description[u"type"]
                  self.itemsToGive[classID]["items"][assetID] = {
                    "craftable": not (u"descriptions" in description and "( Not Usable in Crafting )" in [attribute["value"] for attribute in description[u"descriptions"]]),
                    "tradable": description[u"tradable"],
                    "background_color": description[u"background_color"],
                    "name_color": description[u"name_color"]
                  }

  def API(self, message, parameters):
    parameters['key'] = self.steam["api"]
    data = urllib.urlencode(parameters)
    for i in range(0,3):
      try:
        if "DeclineTradeOffer" in message or "CancelTradeOffer" in message:
          response = self.browser.open("http://api.steampowered.com/" + message + "/", data, timeout = 5.0)
        else:
          response = self.browser.open("http://api.steampowered.com/" + message + "/?" + data, timeout = 5.0)
      except (HTTPError, URLError) as error:
        continue
      response = json.loads(response.read())
      return response
    return False

  def Ajax(self, action, parameters):
    parameters['sessionID'] = self.sessionid
    data = urllib.urlencode(parameters)
    for i in range(0,3):
      try:
        response = self.browser.open("http://steamcommunity.com/actions/" + action, data, timeout = 5.0)
      except (HTTPError, URLError) as error:
        continue
      response = json.loads(response.read())
      return response
    return False

class SID:
  def __init__(self, steamID = False, communityID = False, accountID = False):
    self.steamIDBase = 76561197960265728
    if steamID:
      self.steamID = steamID
    elif communityID:
      account = []
      account.append("STEAM_0:")
      accountLastPart = int(communityID) - self.steamIDBase
      if accountLastPart % 2 == 0:
        account.append("0:")
      else:
        account.append("1:")
      account.append(str(accountLastPart // 2))
      self.steamID = "".join(account)
    elif accountID:
      self.steamID = "STEAM_0:%d:%d" % (accountID & 1, accountID >> 1)

  def toCommunity(self):
    steamIDParts = self.steamID.split(":")
    communityID = int(steamIDParts[2]) * 2
    if steamIDParts[1] == "1":
      communityID += 1
    communityID += self.steamIDBase
    return communityID

  def toSteam(self):
    return steamID

  def toAccount(self):
    steamIDParts = self.steamID.split(":")
    accountID = int(steamIDParts[2]) << 1
    return accountID
