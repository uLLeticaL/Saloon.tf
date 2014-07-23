import logging, simplejson as json

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
    c.match["status"] = RMatch.status
    c.match["time"] = RMatch.time
    if RMatch.Stream:
      c.match["stream"] = RMatch.Stream.channel
      c.match["logs"] = bool(RMatch.Stream.ip)
    c.match["league"] = {}
    c.match["league"]["id"] = RMatch.League.id
    c.match["league"]["name"] = RMatch.League.name
    c.match["league"]["type"] = RMatch.League.type
    c.match["league"]["region"] = RMatch.League.region
    c.match["league"]["colour"] = RMatch.League.colour
    c.match["bet"] = False
    c.match["bets"] = []

    c.match["teamsOrder"] = []
    c.match["teams"] = {}

    betsTotal = 0
    for meta in [[RMatch.Team1, RMatch.BetsTotal1, RMatch.points1, RMatch.points1 > RMatch.points2], [RMatch.Team2, RMatch.BetsTotal2, RMatch.points2, RMatch.points2 > RMatch.points1]]:
      RTeam = meta[0]
      RBetsTotal = meta[1]
      team = {}
      team["id"] = RTeam.id
      team["name"] = RTeam.name
      team["won"] = meta[3]
      team["points"] = meta[2]
      team["bets"] = {}
      team["bets"]["value"] = RBetsTotal.value
      betsTotal += RBetsTotal.value
      c.match["teamsOrder"].append(RTeam.id)
      c.match["teams"][RTeam.id] = team

    if betsTotal > 0:
      for team in c.match["teams"].values():
        team["bets"]["percentage"] = int(round(float(team["bets"]["value"]) / float(betsTotal) * 100))
    else:
      for team in c.match["teams"].values():
        team["bets"]["percentage"] = 0
    c.match["teamsJson"] = json.dumps(c.match["teams"])

    if user:
      RBet = db.Session.query(db.Bets).filter(and_(db.Bets.user == RUser.id, db.Bets.match == RMatch.id)).first()
      if RBet:
        c.match["bet"] = RBet.team
        c.match["betGroups"] = RBet.groups
        c.match["betStatus"] = RBet.status
        if RBet.status == 1 or RBet.status == 2:
          c.match["wonGroups"] = RBet.wonGroups
        if RBet.status == 2:
          c.match["betOffer"] = RBet.offerID
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