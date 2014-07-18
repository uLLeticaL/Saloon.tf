import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render
from sqlalchemy import func, and_
from website.model.user import User
import database as db
import json

log = logging.getLogger(__name__)

class ApiController(BaseController):

  def users(self, name = False, steamid = False, limit = False):
    # Return a json string
    if limit:
      limit = int(limit)
      if limit > 10:
        limit = 10
    print limit
    if name:
      name = name.lower()
      RUsers = db.Session.query(db.Users).filter(func.lower(db.Users.name).like(name + "%")).limit(limit).all()
    else:
      RUsers = db.Session.query(db.Users).filter(db.Users.steamid == steamid).limit(limit).all()

    users = []
    for RUser in RUsers:
      user = {}
      user["id"] = RUser.id
      user["name"] = RUser.name
      user["steamid"] = RUser.steamID
      users.append(user)

    return json.dumps(users)

  def bets(self, betID, offset = 0, limit = 20):
    user = User()
    RMatch = db.Session.query(db.Matches).filter(db.Matches.id == betID).first()
    if user:
      RUser = user[0]
      RBets = db.Session.query(db.Bets).filter(and_(db.Bets.match == betID, db.Bets.user != RUser.id)).order_by(db.Bets.id.desc()).limit(limit).offset(offset).all()
    else:
      RBets = db.Session.query(db.Bets).filter(db.Bets.match == betID).order_by(db.Bets.id.desc()).limit(limit).offset(offset).all()

    bets = []
    for RBet in RBets:
      bet = {}
      bet["user"] = {}
      bet["user"]["id"] = RBet.User.id
      bet["user"]["name"] = RBet.User.name
      bet["team"] = {}
      bet["team"]["id"] = RBet.team
      bet["team"]["name"] = RMatch.Team1.name if RMatch.Team1.id == RBet.team else RMatch.Team2.name
      bet["groups"] = RBet.groups
      bets.append(bet)
    return json.dumps(bets)

  def refreshSession(self):
    db.Session.commit()
    return json.dumps(True)