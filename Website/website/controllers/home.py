import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

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

        RMatches = db.Session.query(db.Matches).limit(10).all()
        RItems = db.Session.query(db.Items).all()
        
        items = {}
        for RItem in RItems:
          items[RItem.assetID] = RItem

        c.matches = []
        for RMatch in RMatches:
          match = {}
          match["id"] = RMatch.id
          match["league"] = {}
          match["league"]["id"] = RMatch.League.id
          match["league"]["name"] = RMatch.League.name
          match["league"]["type"] = RMatch.League.type
          match["league"]["region"] = RMatch.League.region
          match["league"]["colour"] = RMatch.League.colour

          match["teams"] = []
          for RTeam in [RMatch.Team1, RMatch.Team2]:
            team = {}
            team["id"] = RTeam.id
            team["name"] = RTeam.name
            team["bets"] = {}
            match["teams"].append(team)
          c.matches.append(match)

          betsTotal = 0
          for team, RBetsTotal in enumerate([RMatch.BetsTotal1, RMatch.BetsTotal2]):
            bets = 0
            bets += RBetsTotal.metal
            for classID in items:
              RItem = items[classID]
              if not RItem.metal:
                bets += (getattr(RBetsTotal, RItem.name) * RItem.value)
            betsTotal += bets
            match["teams"][team]["bets"]["value"] = bets

          if betsTotal > 0:
            for team in match["teams"]:
              team["bets"]["percentage"] = int(round(float(team["bets"]["value"]) / float(betsTotal) * 100))
          else:
            for team in match["teams"]:
              team["bets"]["percentage"] = 50

        return render('/home.mako')