import re
import os
import time
import json
import base64
import colorama as color
import urllib, cookielib
import settings, utilities
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from mechanize import Browser, HTTPError, URLError

class Bot(object):
  def __init__(self, botID, name, steam, Callback):
    self.id = botID
    self.name = name
    self.steam = steam

    self.Callback = Callback

    self.sessionid = False
    self.cookiejar = cookielib.LWPCookieJar()
    self.cookiefile = "cookies/" + self.steam["login"]
    if os.path.isfile(self.cookiefile):
      self.cookiejar.load(self.cookiefile)

    self.browser = Browser()
    self.browser.set_handle_robots(False)
    self.browser.set_cookiejar(self.cookiejar)

    self.OAuth(self)

  def log(self, message):
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
        self.Bot.log("SteamGuard code needed")
      else:
        self.Bot.log("Encrypting password")
        encrypted = self.encryptPassword(self.Bot.steam["login"], self.Bot.steam["password"].encode("ascii","ignore"))
        self.Bot.log("Logging in")

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
        self.Bot.log("Logging in again with SteamGuard code")
      if captchaNeeded:
        parameters["captchagid"] = captchaGid
        parameters["captcha_text"] = captchaCode

      data = urllib.urlencode(parameters)
      response = self.Bot.browser.open("https://steamcommunity.com/login/dologin/", data)
      response = json.loads(response.read())
      if response[u"success"]:
        self.Bot.sessionid = self.getSessionId()
        self.Bot.cookiejar.save(self.Bot.cookiefile)
        self.Bot.log("Logged in successfully")
        return True
      elif response[u"message"] == u"SteamGuard":
        # Try to log in again using SteamGuard code
        self.signIn(guardNeeded = True, steamID = response[u"emailsteamid"], encrypted = encrypted)
      elif response[u"message"] == u"Error verifying humanity":
        captchaCode = self.Bot.Callback.captchaCode(response[u"captcha_gid"])
        self.signIn(captchaNeeded = True, captchaGid = response[u"captcha_gid"], captchaCode = captchaCode)
      else:
        self.Bot.log("Something went wrong. Message: " + response[u"message"])
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
      sessionId = re.findall(r'g_sessionID = "(.*?)"', response.read())[0]
      return sessionId

  class OCommunity(object):
    def __init__(self, bot):
      self.Bot = bot

    def GetFriends(self, steamID = False, prefetch = False):
      if steamID:
        return self.Friend(steamID, self.Bot)
      else:
        parameters = {'relationship': 'friend', 'steamid': self.Bot.steam["id"]}
        response = self.Bot.API("ISteamUser/GetFriendList/v0001", parameters)
        friends = []
        if prefetch:
          steamIDs = []
          blocks = []
          count = 0
        for friend in response[u"friendslist"][u"friends"]:
          steamID = friend[u"steamid"].encode('ascii', 'ignore')
          friends.append(self.Friend(steamID, self.Bot))
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
              friends[count].loaded = True
              count += 1
        return friends

    class Friend:
      def __init__(self, steamID, bot):
        self.steamID = steamID
        self.loaded = False
        self.Bot = bot

      def add(self):
        parameters = {
          'steamid': self.steamID,
          'accept_invite': 0
        }
        response = self.Bot.Ajax('AddFriendAjax', parameters)
        if response:
          return True
          self.Bot.log("Sent friend request to " + self.steamID)
        else:
          return False
          self.Bot.log("Couldn't add " + self.steamID + " to the friends list.")

      def accept(self):
        parameters = {
          'steamid': self.steamID,
          'accept_invite': 1
        }
        response = self.Bot.Ajax('AddFriendAjax', parameters)
        if response:
          self.Bot.log("Accepted friend request from " + self.steamID)
          return True
        else:
          self.Bot.log("Couldn't add " + self.steamID + " to the friends list.")
          return False

      def remove(self):
        parameters = {
          'steamid': self.steamID
        }
        response = self.Bot.Ajax('RemoveFriendAjax', parameters)
        if response:
          self.Bot.log("Removed " + self.steamID + " from the friends list.")
          return True
        else:
          self.Bot.log("Couldn't remove " + self.steamID + " from the friends list.")
          return False

      def summary(self):
        if self.loaded is False:
          parameters = {'steamids': self.steamID}
          response = self.Bot.API("ISteamUser/GetPlayerSummaries/v0002", parameters)
          if len(response[u"response"][u"players"]) is 1:
            player = response[u"response"][u"players"][0]
            self.name = player[u"personaname"]
            self.state = player[u"personastate"]
            self.avatar = player[u"avatarfull"]
            self.public = True if player[u"communityvisibilitystate"] is 3 else False
            self.loaded = True
        return {
          'name': self.name,
          'state': self.state,
          'avatar': self.avatar,
          'public': self.public
        }

  class OTrade(object):
    def __init__(self, bot):
      self.Bot = bot
      self.offersCache = {}

    def MakeOffer(self, Partner, scraps = 0, keys = 0):
      return False

    def GetOffers(self, offerType = "received", offerState = 2, ID = False):
      if ID:
        parameters = {'tradeofferid': str(ID)}
        response = self.Bot.API("IEconService/GetTradeOffer/v0001", parameters)
        response = respsonse[u"response"]
      else:
        parameters = {
          'active_only': 1,
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
            if offerID in self.offersCache:
              offers[offerID] = self.offersCache[offerID]
            else:
              accountID = offer[u"accountid_other"]
              partnerID = "STEAM_0:%d:%d" % (accountID & 1, accountID >> 1)
              partnerID = SID(partnerID).toCommunity()
              Partner = self.Bot.Community().GetFriends(steamID = str(partnerID))

              itemsToGive = []
              if u"items_to_give" in offer:
                broken = False
                for item in offer[u"items_to_give"]:
                  classID = item[u"classid"].encode('ascii', 'ignore')
                  amount = int(item[u"amount"])
                  itemsToGive.append([amount, classID])

              itemsToReceive = []
              if u"items_to_receive" in offer:
                broken = False
                for item in offer[u"items_to_receive"]:
                  classID = item[u"classid"].encode('ascii', 'ignore')
                  amount = int(item[u"amount"])
                  itemsToReceive.append([amount, classID])

              offer = self.Offer(offerID, self.Bot, Partner = Partner)
              offer.itemsToGive = itemsToGive
              offer.itemsToReceive = itemsToReceive
              offers[offerID] = offer

        if ID and ID not in offersCache:
          self.offersCache[ID] = offers[ID]
        else:
          self.offersCache = offers
        return offers
      else:
        return False

    class Offer:
      def __init__(self, offerID, bot, Partner = False):
        self.offerID = offerID
        self.Partner = Partner
        self.Bot = bot
        self.itemsToGive = []
        self.itemsToReceive = []

      def accept(self):
        self.Bot.browser.addheaders = [('Referer', "https://steamcommunity.com/tradeoffer/" + str(self.offerID))]
        parameters = {
          'partner': self.Partner.steamID.encode("utf-8"),
          'tradeofferid': str(self.offerID).encode("utf-8"),
          'sessionid': self.Bot.sessionid.encode("utf-8")
        }

        data = urllib.urlencode(parameters)
        try:
          response = self.Bot.browser.open("https://steamcommunity.com/tradeoffer/" + str(self.offerID) + "/accept", data)
        except (HTTPError, URLError) as error:
          return False
          self.Bot.log("Couldn't accept #" + str(self.offerID) + " offer. " + str(error.code) + " ERROR.")
        else:
          return True
          self.Bot.log("Accepted #" + str(self.offerID) + " offer.")

      def decline(self):
        parameters = {
          'tradeofferid': str(self.offerID)
        }
        response = self.Bot.API("IEconService/DeclineTradeOffer/v1", parameters)
        if response:
          return True
          self.Bot.log("Declined #" + str(self.offerID) + " offer.")
        else:
          return False
          self.Bot.log("Couldn't decline #" + str(self.offerID) + " offer. " + str(error.code) + " ERROR.")

  def API(self, message, parameters):
    parameters['key'] = self.steam["api"]
    data = urllib.urlencode(parameters)
    try:
      response = self.browser.open("http://api.steampowered.com/" + message + "/?" + data, timeout = 1.0)
    except (HTTPError, URLError) as error:
      return False
    else:
      response = json.loads(response.read())
      return response

  def Ajax(self, action, parameters):
    parameters['sessionID'] = self.sessionid
    data = urllib.urlencode(parameters)
    try:
      response = self.browser.open("http://steamcommunity.com/actions/" + action, data)
    except (HTTPError, URLError) as error:
      return False
    else:
      response = json.loads(response.read())
      return response

class SID:
  def __init__(self, steamID):
    self.steamIDBase = 76561197960265728
    self.steamID = steamID

  def toCommunity(self):
    steamIDParts = re.split(":", self.steamID)
    community = int(steamIDParts[2]) * 2
    if steamIDParts[1] == "1":
      community += 1
    community += self.steamIDBase
    return community

  def toSteam(self):
    account = []
    account.append("STEAM_0:")
    accountLastPart = self.steamID - steamIDBase
    if steamIDLastPart % 2 == 0:
      account.append("0:")
    else:
      account.append("1:")
    account.append(str(accountLastPart // 2))
    return "".join(account)