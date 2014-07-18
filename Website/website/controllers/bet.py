import logging

from sqlalchemy.sql.expression import tuple_
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from collections import defaultdict, Counter
from sqlalchemy import and_
from website.lib.base import BaseController, render
from website.model.user import User
import database as db

log = logging.getLogger(__name__)

class BetController(BaseController):

  def index(self, betID):
    # Return a rendered template
    #return render('/bet.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      c.user = user[1]
    else:
      c.user = False
    c.current = "bet"

    RMatch = db.Session.query(db.Matches).filter(db.Matches.id == betID).first()
    RItems = db.Session.query(db.Items).all()

    items = defaultdict(dict)
    for RItem in RItems:
      items[RItem.defindex][RItem.quality] = RItem

    c.match = {}
    c.match = {}
    c.match["id"] = RMatch.id
    c.match["league"] = {}
    c.match["league"]["id"] = RMatch.League.id
    c.match["league"]["name"] = RMatch.League.name
    c.match["league"]["type"] = RMatch.League.type
    c.match["league"]["region"] = RMatch.League.region
    c.match["league"]["colour"] = RMatch.League.colour
    c.match["bets"] = []
    c.match["ownbet"] = False

    c.match["teams"] = []
    for RTeam in [RMatch.Team1, RMatch.Team2]:
      team = {}
      team["id"] = RTeam.id
      team["name"] = RTeam.name
      team["bets"] = {}
      c.match["teams"].append(team)

    betsTotal = 0
    for team, RBetsTotal in enumerate([RMatch.BetsTotal1, RMatch.BetsTotal2]):
      betsTotal += RBetsTotal.value
      c.match["teams"][team]["bets"]["value"] = RBetsTotal.value
    if betsTotal > 0:
      for team in c.match["teams"]:
        team["bets"]["percentage"] = int(round(float(team["bets"]["value"]) / float(betsTotal) * 100))
    else:
      for team in c.match["teams"]:
        team["bets"]["percentage"] = 0

    if c.user:
      RBet = db.Session.query(db.Bets).filter(and_(db.Bets.user == user[0].id, db.Bets.match == RMatch.id)).first()
      if RBet:
        c.match["ownbet"] = {}
        c.match["ownbet"]["user"] = {}
        c.match["ownbet"]["user"]["id"] = RUser.id
        c.match["ownbet"]["team"] = {}
        c.match["ownbet"]["team"]["id"] = RBet.team
        c.match["ownbet"]["team"]["name"] = RMatch.Team1.name if RMatch.Team1.id == RBet.team else RMatch.Team2.name
        c.match["ownbet"]["groups"] = RBet.groups

    return render('/bet.mako')

  def switch(self, betID):
    # Return redirect('/bet/' + betID + '/')
    user = User()
    if user:
      RUser = user[0]
      c.user = user[1]
      RMatch = db.Session.query(db.Matches).filter(db.Matches.id == betID).first()
      if RMatch:
        RBet = db.Session.query(db.Bets).filter(and_(db.Bets.match == RMatch.id, db.Bets.user == RUser.id)).first()
        if RBet.team == RMatch.team1:
          RBetsTotal1 = db.Session.query(db.BetsTotal).filter(and_(db.BetsTotal.match == RMatch.id, db.BetsTotal.team == RMatch.team1)).first()
          RBetsTotal2 = db.Session.query(db.BetsTotal).filter(and_(db.BetsTotal.match == RMatch.id, db.BetsTotal.team == RMatch.team2)).first()
          RBet.team = RMatch.team2
        else:
          RBetsTotal1 = db.Session.query(db.BetsTotal).filter(and_(db.BetsTotal.match == RMatch.id, db.BetsTotal.team == RMatch.team2)).first()
          RBetsTotal2 = db.Session.query(db.BetsTotal).filter(and_(db.BetsTotal.match == RMatch.id, db.BetsTotal.team == RMatch.team1)).first()
          RBet.team = RMatch.team1

        RBetsTotal1.value -= RBet.value
        RBetsTotal2.value += RBet.value

        keys = []
        totalGroups1 = defaultdict(Counter)
        for group in RBetsTotal1.groups:
          totalGroups1[group[0]][group[1]] = group[2]
          keys.append((group[0], group[1]))

        totalGroups2 = defaultdict(Counter)
        for group in RBetsTotal2.groups:
          totalGroups2[group[0]][group[1]] = group[2]
          keys.append((group[0], group[1]))
        
        # Convert PostgreSQL's multidimensional array to dictionary
        usersGroups = defaultdict(Counter)
        for group in RBet.groups:
          totalGroups1[group[0]][group[1]] -= group[2]
          totalGroups2[group[0]][group[1]] += group[2]

        orderedGroups1 = []
        orderedGroups2 = []
        orderedItems = db.Session.query(db.Items).filter(tuple_(db.Items.defindex, db.Items.quality).in_(keys)).order_by(db.Items.type, db.Items.quality, db.Items.value.desc()).all()
        for orderedItem in orderedItems:
          defindex = orderedItem.defindex
          quality = orderedItem.quality
          if quality in totalGroups1[defindex]:
            orderedGroups1.append([defindex, quality, totalGroups1[defindex][quality]])
          if quality in totalGroups2[defindex]:
            orderedGroups2.append([defindex, quality, totalGroups2[defindex][quality]])
        RBetsTotal1.groups = orderedGroups1
        RBetsTotal2.groups = orderedGroups2

        db.Session.commit()
        return redirect('/bet/' + betID + '/')
    return redirect('/')