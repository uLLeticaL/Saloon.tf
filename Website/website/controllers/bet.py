import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render
from website.model.user import User
import database as db

log = logging.getLogger(__name__)

class BetController(BaseController):

    def index(self, id):
        # Return a rendered template
        #return render('/bet.mako')
        # or, return a string
        user = User()
        if user:
          c.user = user[1]
        else:
          c.user = False
        c.current = "bet"

        RMatch = db.Session.query(db.Matches).first()
        RItems = db.Session.query(db.Items).all()

        items = {}
        for RItem in RItems:
          items[RItem.assetID] = RItem

        c.match = {}
        c.match = {}
        c.match["id"] = RMatch.id
        c.match["league"] = {}
        c.match["league"]["id"] = RMatch.League.id
        c.match["league"]["name"] = RMatch.League.name
        c.match["league"]["type"] = RMatch.League.type
        c.match["league"]["region"] = RMatch.League.region
        c.match["league"]["colour"] = RMatch.League.colour

        c.match["teams"] = []
        for RTeam in [RMatch.Team1, RMatch.Team2]:
          team = {}
          team["id"] = RTeam.id
          team["name"] = RTeam.name
          team["bets"] = {}
          c.match["teams"].append(team)

        betsTotal = 0
        for team, RBetsTotal in enumerate([RMatch.BetsTotal1, RMatch.BetsTotal2]):
          bets = 0
          bets += RBetsTotal.metal
          for classID in items:
            RItem = items[classID]
            if not RItem.metal:
              bets += (getattr(RBetsTotal, RItem.name) * RItem.value)
          betsTotal += bets
          c.match["teams"][team]["bets"]["value"] = bets

        if betsTotal > 0:
          for team in c.match["teams"]:
            team["bets"]["percentage"] = int(round(float(team["bets"]["value"]) / float(betsTotal) * 100))
        else:
          for team in c.match["teams"]:
            team["bets"]["percentage"] = 50

        return render('/bet.mako')