import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sqlalchemy import and_
from website.lib.base import BaseController, render
from website.model.user import User
import database as db

log = logging.getLogger(__name__)

class HomeController(BaseController):

  def index(self):
    # Return a rendered template
    #return render('/home.mako')
    # or, return a string
    user = User()
    if user:
      c.user = user[1]
    else:
      c.user = False
    c.current = "home"

    RMatches = db.Session.query(db.Matches).order_by(db.Matches.id.desc()).limit(10).all()

    c.matches = []
    for RMatch in RMatches:
      match = {}
      match["id"] = RMatch.id
      match["status"] = RMatch.status
      match["time"] = RMatch.time
      match["league"] = {}
      match["league"]["id"] = RMatch.League.id
      match["league"]["name"] = RMatch.League.name
      match["league"]["type"] = RMatch.League.type
      match["league"]["region"] = RMatch.League.region
      match["league"]["colour"] = RMatch.League.colour
      match["bet"] = False

      match["teamsOrder"] = []
      match["teams"] = {}

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
        match["teamsOrder"].append(RTeam.id)
        match["teams"][RTeam.id] = team

      betsTotal = 0
      for RBetsTotal in [RMatch.BetsTotal1, RMatch.BetsTotal2]:
        betsTotal += RBetsTotal.value
        match["teams"][RBetsTotal.team]["bets"]["value"] = RBetsTotal.value
      if betsTotal > 0:
        for team in match["teams"].values():
          team["bets"]["percentage"] = int(round(float(team["bets"]["value"]) / float(betsTotal) * 100))
      else:
        for team in match["teams"].values():
          team["bets"]["percentage"] = 0

      if c.user:
        RBet = db.Session.query(db.Bets).filter(and_(db.Bets.user == user[0].id, db.Bets.match == RMatch.id)).first()
        if RBet:
          match["bet"] = RBet.team
      c.matches.append(match)
    return render('/home.mako')