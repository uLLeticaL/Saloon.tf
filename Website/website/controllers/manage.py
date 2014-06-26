import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render
from website.model.user import User
import database as db
import json
import os

log = logging.getLogger(__name__)

class ManageController(BaseController):

  def index(self):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "dashboard"
        return render('/manage/dashboard.mako')
      else:
        return redirect('http://saloon.tf/home/')
    else:
      return redirect('http://saloon.tf/home/')

  def leagues(self):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "leagues"

        RLeagues = db.Session.query(db.Leagues).order_by(db.Leagues.id).limit(10).all()
        c.leagues = []
        for RLeague in RLeagues:
          league = {}
          league["id"] = RLeague.id
          league["name"] = RLeague.name
          league["type"] = RLeague.type
          league["region"] = RLeague.region
          league["colour"] = RLeague.colour
          league["json"] = json.dumps(league)
          c.leagues.append(league)

        if hasattr(session, "failed"):
          c.failed = True
          c.action = session.action
          c.message = session.message
          c.name = session.name
          c.type = session.type
          c.region = session.region
          c.accentColour = session.accentColour

        return render('/manage/leagues.mako')
      else:
        return redirect('http://saloon.tf/home/')
    else:
      return redirect('http://saloon.tf/home/')

  def addLeague(self):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        params = ["name", "type", "region", "avatar", "accentColour"]
        if all(item in request.params for item in params):
          if request.params["avatar"].filename[-4:] != ".png":
            success = False
            message = "Wrong file type."
          else:
            RLeague = db.Leagues(name=request.params["name"], type=request.params["type"], region=request.params["region"], colour=request.params["accentColour"])
            db.Session.add(RLeague)
            db.Session.commit()
            os.makedirs("website/public/images/leagues/" + str(RLeague.id))

            avatar = request.params["avatar"].file
            avatar_path = os.path.join('website/public/images/leagues', str(RLeague.id), 'logo.png')
            print avatar_path
            temp_path = avatar_path + '~'
            output_file = open(temp_path, 'wb')
            avatar.seek(0)
            while True:
              data = avatar.read(2<<16)
              if not data:
                break
              output_file.write(data)
            output_file.close()
            os.rename(temp_path, avatar_path)
            return redirect("/manage/leagues")
        else:
          return redirect("/manage/leagues")
      else:
        return redirect("/")
    else:
      return redirect("/")

  def removeLeague(self, id):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        RLeague = db.Session.query(db.Leagues).filter(db.Leagues.id == id).first()
        if RLeague:
          db.Session.delete(RLeague)
          db.Session.commit()
          success = True
          message = "Removed selected league."
        else:
          success = False
          message = "<strong>Oh snap!</strong> Couldn't remove this league."
    else:
      success = False
      message = "You don't have sufficent priviledges to access this page."
    array = {"success": success, "message": message}
    return json.dumps(array)

  def editLeague(self, id):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        RLeague = db.Session.query(db.Leagues).filter(db.Leagues.id == id).first()
        print request.params
        if RLeague:
          RLeague.name = request.params["name"]
          RLeague.type = request.params["type"]
          RLeague.region = request.params["region"]
          RLeague.colour = request.params["accentColour"]
          db.Session.commit()
          success = True
          message = "Changed selected league."
        else:
          success = False
          message = "<strong>Oh snap!</strong> Couldn't change this league."
    else:
      success = False
      message = "You don't have sufficent priviledges to access this page."
    array = {"success": success, "message": message}
    return json.dumps(array)

  def teamsLeagues(self):
    # Return a rendered template
    #return render('manage/teams.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "teams"

        RLeagues = db.Session.query(db.Leagues).order_by(db.Leagues.id).limit(10).all()
        c.leagues = []
        for RLeague in RLeagues:
          league = {}
          league["id"] = RLeague.id
          league["name"] = RLeague.name
          league["type"] = RLeague.type
          league["region"] = RLeague.region
          league["colour"] = RLeague.colour
          league["json"] = json.dumps(league)
          c.leagues.append(league)

        return render('/manage/teams/index.mako')
      else:
        return redirect('http://saloon.tf/home/')
    else:
      return redirect('http://saloon.tf/home/')

  def teamsList(self, leagueID):
    # Return a rendered template
    #return render('manage/teams.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "teams"

        RLeague = db.Session.query(db.Leagues).filter(db.Leagues.id == leagueID).first()
        RTeams = db.Session.query(db.Teams).filter(db.Teams.league == leagueID).order_by(db.Teams.id).limit(10).all()
        RCountries = db.Session.query(db.Countries).order_by(db.Countries.name).all()

        c.league = {}
        c.league["id"] = RLeague.id
        c.league["name"] = RLeague.name
        c.league["type"] = RLeague.type
        c.league["region"] = RLeague.region
        c.league["colour"] = RLeague.colour

        c.teams = []
        for RTeam in RTeams:
          team = {}
          team["id"] = RTeam.id
          team["name"] = RTeam.name
          team["leagueID"] = RTeam.leagueID
          team["country"] = RTeam.Country.name
          team["countryID"] = RTeam.Country.id
          team["json"] = json.dumps(team)
          c.teams.append(team)
        
        c.countries = []
        for RCountry in RCountries:
          country = {}
          country["id"] = RCountry.id
          country["name"] = RCountry.name
          c.countries.append(country)

        return render('/manage/teams/list.mako')
      else:
        return redirect('http://saloon.tf/home/')
    else:
      return redirect('http://saloon.tf/home/')

  def addTeam(self, leagueID):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        RTeam = db.Teams(name=request.params["name"], country=request.params["country"], league=leagueID, leagueID=request.params["leagueID"])
        db.Session.add(RTeam)
        db.Session.commit()

        avatar = request.params["avatar"].file
        avatar_path = os.path.join('website/public/images/teams', str(RTeam.id) + '.jpg')
        print avatar_path
        temp_path = avatar_path + '~'
        output_file = open(temp_path, 'wb')
        avatar.seek(0)
        while True:
          data = avatar.read(2<<16)
          if not data:
            break
          output_file.write(data)
        output_file.close()
        os.rename(temp_path, avatar_path)
        return redirect("/manage/teams/" + leagueID)
      else:
        return redirect("/")
    else:
      return redirect("/")

  def editTeam(self, leagueID, teamID):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        RTeam = db.Session.query(db.Teams).filter(db.Teams.id == teamID).first()
        if (RTeam):
          RTeam.name = request.params["name"]
          RTeam.country = request.params["country"]
          RTeam.league = leagueID,
          RTeam.leagueID = request.params["leagueID"]
          db.Session.commit()
          success = True
          message = "Changed selected league."
        else:
          success = False
          message = "<strong>Oh snap!</strong> Couldn't edit this team."
      else:
        success = False
        message = "You don't have sufficent priviledges to access this page."
    else:
      success = False
      message = "You don't have sufficent priviledges to access this page."
    array = {"success": success, "message": message}
    return json.dumps(array)

  def removeTeam(self, leagueID, teamID):
    # Return a rendered template
    #return render('/manage.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        RTeam = db.Session.query(db.Teams).filter(db.Teams.id == teamID).first()
        if RTeam:
          RMatch = db.Session.query(db.Matches).filter(db.or_(db.Matches.team1 == teamID, db.Matches.team2 == teamID)).first()
          if RMatch:
            success = False
            message = "<strong>Oh snap!</strong> I can't remove a team with matches."
          else:
            db.Session.delete(RTeam)
            db.Session.commit()
            success = True
            message = "Removed selected team."
        else:
          success = False
          message = "<strong>Oh snap!</strong> Couldn't remove this team."
      else:
        success = False
        message = "You don't have sufficent priviledges to access this page."
    else:
      success = False
      message = "You don't have sufficent priviledges to access this page."

    array = {"success": success, "message": message}
    return json.dumps(array)

  def matchesLeagues(self):
    # Return a rendered template
    #return render('manage/teams.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "matches"

        RLeagues = db.Session.query(db.Leagues).order_by(db.Leagues.id).limit(10).all()
        c.leagues = []
        for RLeague in RLeagues:
          league = {}
          league["id"] = RLeague.id
          league["name"] = RLeague.name
          league["type"] = RLeague.type
          league["region"] = RLeague.region
          league["colour"] = RLeague.colour
          league["json"] = json.dumps(league)
          c.leagues.append(league)

        return render('/manage/matches/index.mako')
      else:
        return redirect('http://saloon.tf/home/')
    else:
      return redirect('http://saloon.tf/home/')

  def matchesList(self, leagueID):
    # Return a rendered template
    #return render('manage/teams.mako')
    # or, return a string
    user = User()
    if user:
      RUser = user[0]
      if RUser.level <= 3:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "matches"

        RLeague = db.Session.query(db.Leagues).filter(db.Leagues.id == leagueID).first()
        RMatches = db.Session.query(db.Matches).filter(db.Matches.league == leagueID).order_by(db.Matches.id).limit(10).all()
        RTeams = db.Session.query(db.Teams).filter(db.Teams.league == leagueID).order_by(db.Teams.id).all()

        c.league = {}
        c.league["id"] = RLeague.id
        c.league["name"] = RLeague.name
        c.league["type"] = RLeague.type
        c.league["region"] = RLeague.region
        c.league["colour"] = RLeague.colour

        c.matches = []
        for RMatch in RMatches:
          match = {}
          match["id"] = RMatch.id
          match["stream"] = RMatch.stream
          match["won"] = RMatch.won

          match["team1"] = {}
          match["team1"]["id"] = RMatch.Team1.id
          match["team1"]["name"] = RMatch.Team1.name
          match["team1"]["country"] = RMatch.Team1.Country.name
          match["team1"]["countryID"] = RMatch.Team1.Country.id

          match["team2"] = {}
          match["team2"]["id"] = RMatch.Team2.id
          match["team2"]["name"] = RMatch.Team2.name
          match["team2"]["country"] = RMatch.Team2.Country.name
          match["team2"]["countryID"] = RMatch.Team2.Country.id

          match["json"] = json.dumps(match)
          c.matches.append(match)
        print c.matches
        c.teams = []
        for RTeam in RTeams:
          team = {}
          team["id"] = RTeam.id
          team["name"] = RTeam.name
          c.teams.append(team)

        return render('/manage/matches/list.mako')
      else:
        return redirect('http://saloon.tf/home/')
    else:
      return redirect('http://saloon.tf/home/')