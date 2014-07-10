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
      user["permissions"] = RUser.Permissions[0]
      user["botID"] = RUser.bot
    else:
      url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%d" % (config["steamapi"], user["steamid"])
      data = json.loads(requests.get(url).text)[u"response"][u"players"][0]
      user["avatar"] = "http://media.steampowered.com/steamcommunity/public/images/avatars/" + data[u"avatarfull"][67:-9] + "_full.jpg"
      user["name"] = data[u"personaname"]
      user["botID"] = randrange(1, db.Session.query(func.count(db.Bots.id)).scalar())
      RUser = db.Users(name = user["name"], avatar = data[u"avatarfull"][67:-9], steamID = user["steamid"], bot = user["botID"])
      db.Session.add(RUser)
      db.Session.commit()
      user["id"] = RUser.id
      RUserPermissions = db.UsersPermissions(user = user["id"], manage = False, leagues = False, teams = False, users = False, bets = False, bots = False, permissions = False)
      db.Session.add(RUserPermissions)
      db.Session.commit()
      user["items"] = RUser.Items[0]
      user["permissions"] = RUser.Permissions[0]
    return [RUser, user]
  else:
    return False