from pylons import request, response, session, tmpl_context as c, url, config
import json, requests
import database as db
from random import randrange
from sqlalchemy import func

def User():
  user = {}
  if "steamid" in session:
    user["steamid"] = session["steamid"]
    RUser = db.Session.query(db.Users).filter(db.Users.steamID == user["steamid"]).first()
    if RUser:
      user["id"] = RUser.id
      user["name"] = RUser.name
      user["avatar"] = "http://media.steampowered.com/steamcommunity/public/images/avatars/" + RUser.avatar + "_full.jpg"
      user["items"] = RUser.Items[0]
      user["permissions"] = RUser.Permissions[0]
    else:
      url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%d" % (config["steamapi"], user["steamid"])
      data = requests.get(url).text
      player = json.loads(data)[u"response"][u"players"][0]
      user["avatar"] = "http://media.steampowered.com/steamcommunity/public/images/avatars/" + player[u"avatarfull"][67:-9] + "_full.jpg"
      user["name"] = player[u"personaname"]
      botID = randrange(1, db.Session.query(func.count(db.Bots)).scalar())
      RUser = db.Users(name = user["name"], avatar = player[u"avatarfull"][67:-9], steamID = user["steamid"], bot = botID)
      db.Session.add(RUser)
      db.Session.commit()
      user["id"] = RUser.id
      RUserItems = db.UsersItems(user = user["id"], keys = 0, metal = 0)
      RUserPermissions = db.UsersPermissions(user = user["id"], manage = False, leagues = False, teams = False, users = False, bets = False, bots = False)
      db.Session.add(RUserItems)
      db.Session.add(RUserPermissions)
      db.Session.commit()
      user["items"] = RUser.Items[0]
      user["permissions"] = RUser.Permissions[0]
    return [RUser, user]
  else:
    return False