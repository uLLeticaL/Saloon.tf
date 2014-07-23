import logging

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render
from website.model.user import User
import database as db
import json
import os

log = logging.getLogger(__name__)

class ManageController(BaseController):

  def index(self):
    # Returns a rendered template
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].manage:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "dashboard"
        return render('/manage/dashboard.mako')
      else:
        return redirect('/home/')
    else:
      return redirect('/home/')

  def leagues(self):
    # Returns a rendered template
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].leagues:
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
        return redirect('/home/')
    else:
      return redirect('/home/')

  def addLeague(self):
    # Returns redirection to /manage/leagues
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].leagues:
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
    # Returns a json string
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].leagues:
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
    # Returns a json string
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].leagues:
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
    # Returns a rendered template
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].teams:
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
        return redirect('/home/')
    else:
      return redirect('/home/')

  def teamsList(self, leagueID):
    # Returns a rendered template
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].teams:
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
        return redirect('/home/')
    else:
      return redirect('/home/')

  def addTeam(self, leagueID):
    # Returns a redirection to /manage/teams/{leagueID}
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].teams:
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
    # Returns a json string
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].teams:
        RTeam = db.Session.query(db.Teams).filter(db.Teams.id == teamID).first()
        if (RTeam):
          RTeam.name = request.params["name"]
          print type(request.params["name"])
          print type(RTeam.name)
          RTeam.country = request.params["country"]
          RTeam.league = leagueID,
          RTeam.leagueID = request.params["leagueID"]
          db.Session.commit()
          success = True
          message = "Changed selected team."
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
    # Returns a json string
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].teams:
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
    # Returns a rendered template
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].bets:
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
        return redirect('/home/')
    else:
      return redirect('/home/')

  def matchesList(self, leagueID):
    # Returns a rendered template
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].bets:
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
          match["channel"] = RMatch.Stream.channel
          match["ip"] = RMatch.Stream.ip
          match["port"] = RMatch.Stream.port
          match["logsecret"] = RMatch.Stream.logsecret

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
        return redirect('/home/')
    else:
      return redirect('/home/')

  def addMatch(self, leagueID):
    # Returns a redirection to matches
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].bets:
        RMatch = db.Matches(league=leagueID, team1=request.params["team1"], team2=request.params["team2"], stream=request.params["stream"])
        db.Session.add(RMatch)
        db.Session.commit()
        RBetsTotal1 = db.BetsTotal(match=RMatch.id, team=request.params["team1"], value=0, groups=[])
        RBetsTotal2 = db.BetsTotal(match=RMatch.id, team=request.params["team2"], value=0, groups=[])
        db.Session.add(RBetsTotal1)
        db.Session.add(RBetsTotal2)
        RStream = db.Streams(match=RMatch.id, channel=request.params["channel"], ip=request.params["ip"], port=request.params["port"], rcon=request.params["rcon"], logsecret=request.params["logsecret"])
        db.Session.add(RStream)
        db.Session.commit()
        return redirect("/manage/matches/")
      else:
        return redirect("/")
    else:
      return redirect("/")

  def editMatch(self, leagueID, matchID):
    # Returns a json string
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].bets:
        RMatch = db.Session.query(db.Matches).filter(db.Matches.id == matchID).first()
        if RMatch:
          RMatch.league = leagueID
          RMatch.team1 = request.params["team1"]
          RMatch.team2 = request.params["team2"]
          RMatch.Stream.channel = request.params["channel"]
          RMatch.Stream.ip = request.params["ip"]
          RMatch.Stream.port = request.params["port"]
          RMatch.Stream.rcon = request.params["rcon"]
          RMatch.Stream.logsecret = request.params["logsecret"]
          db.Session.commit()
          success = True
          message = "Changed selected match."
        else:
          success = False
          message = "<strong>Oh snap!</strong> Couldn't edit this match."
      else:
        success = False
        message = "You don't have sufficent priviledges to access this page."
    else:
      success = False
      message = "You don't have sufficent priviledges to access this page."
    array = {"success": success, "message": message}
    return json.dumps(array)

  def removeMatch(self, leagueID, matchID):
    # Returns a json string
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].bets:
        RMatch = db.Session.query(db.Matches).filter(db.Matches.id == matchID).first()
        if RMatch:
          db.Session.delete(RMatch)
          db.Session.commit()
          success = True
          message = "Removed selected match."
        else:
          success = False
          message = "<strong>Oh snap!</strong> Couldn't remove this match."
      else:
        success = False
        message = "You don't have sufficent priviledges to access this page."
    else:
      success = False
      message = "You don't have sufficent priviledges to access this page."

    array = {"success": success, "message": message}
    return json.dumps(array)

  def users(self):
    # Returns rendered template
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].users:
        c.user = user[1]
        c.current = "manage"
        c.managePage = "users"
        return render('/manage/users/index.mako')
      else:
        return redirect("/")
    else:
      return redirect("/")

  def user(self, userID):
    user = User()
    if user:
      RUser = user[0]
      if RUser.Permissions[0].users:
        ROtherUser = db.Session.query(db.Users).filter(db.Users.id == userID).first()
        if ROtherUser:
          if request.POST:
            if int(request.POST["steamid"]) != ROtherUser.steamID:
              url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%d" % (config["steamapi"], int(request.POST["steamid"]))
              data = json.loads(requests.get(url).text)[u"response"][u"players"][0]
              ROtherUser.avatar = data[u"avatarfull"][67:-9] + "_full.jpg"
              ROtherUser.name = data[u"personaname"]
              ROtherUser.steamID = request.POST["steamid"]
            if RUser.Permissions[0].permissions:
              for permission in ["manage", "leagues", "teams", "users", "bets", "bots"]:
                if permission not in request.POST.getall("permissions"):
                  setattr(ROtherUser.Permissions[0], permission, False)
                else:
                  setattr(ROtherUser.Permissions[0], permission, True)

            ROtherUser.bot = int(request.POST["botID"])

          c.user = user[1]
          c.otherUser = {}
          c.otherUser["id"] = ROtherUser.id
          c.otherUser["name"] = ROtherUser.name
          c.otherUser["steamid"] = ROtherUser.steamID
          c.otherUser["botID"] = ROtherUser.bot
          c.otherUser["permissions"] = ROtherUser.Permissions[0]

          c.current = "manage"
          c.managePage = "users"

          RBots = db.Session.query(db.Bots).order_by(db.Bots.id).all()
          c.bots = []
          for RBot in RBots:
            bot = {}
            bot["id"] = RBot.id
            bot["name"] = RBot.name
            c.bots.append(bot)

          if request.POST:
            db.Session.commit()

          return render('/manage/users/user.mako')
        else:
          return redirect("/manage/users/")
      else: 
        return redirect("/")
    else: 
      return redirect("/")
