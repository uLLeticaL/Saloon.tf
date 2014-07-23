from SRCDS import SourceServer, SourceServerError
from twisted.internet.protocol import DatagramProtocol
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from threading import Timer
import database as db
import uuid, re

class Handler(object):
  def __init__(self, Broadcast, reactor):
    self.Broadcast = Broadcast
    self.servers = {}
    Stream = aliased(db.Streams)
    RMatches = db.Session.query(db.Matches).filter(and_(db.Matches.status == 1, db.Matches.Stream.has(db.Streams.ip != None))).all()
    for RMatch in RMatches:
      self.addMatch(RMatch.league, RMatch.id, RMatch.Stream.ip.encode("ascii", "ignore"), RMatch.Stream.port, RMatch.Stream.rcon.encode("ascii", "ignore"), RMatch.Stream.logsecret)
    reactor.listenUDP(9001, LogsProtocol(self))

  def addMatch(self, leagueID, matchID, ip, port, rcon = False, logsecret = False):
    host = "%s:%d" % (ip, port)
    self.Broadcast.log(str(matchID), "Adding match on %s" % host)
    self.Broadcast.addMatch(matchID)
    if rcon and not logsecret:
      try:
        server = SourceServer(ip, port)
        server.setRconPassword(rcon)
        match = re.search(r"\"sv_logsecret\" = \"(.*?)\"", server.rcon("sv_logsecret"))
        if match.group(1) == "0":
          logsecret = str(uuid.uuid4())
          server.rcon("sv_logsecret " + logsecret)
        elif match.group(1)[0].lower() not in "abcdefghijklmnopqrstuvxyz":
          logsecret = match.group(1)
        server.rcon("logaddress_add direct.saloon.tf:9001")
      except SourceServerError:
        pass
    self.servers[host] = {
      "matchID": matchID,
      "leagueID": leagueID,
      "logsecret": logsecret
    }

  def logline(self, host, logsecret, line):
    if host in self.servers:
      server = self.servers[host]
      if server["logsecret"] == logsecret:
        matchID = server["matchID"]
        match = re.search(r": \"(.*)<([0-9]+)><(STEAM_[0-1]:[0-1]:[0-9]+)><(Blue|Red)>\" killed \"(.*)<([0-9]+)><(STEAM_[0-1]:[0-1]:[0-9]+)><(Blue|Red)>\" with \"(.*?)\"", line)
        if match:
          name1 = re.sub("(@[A-Za-z0-9]+)|(twitch.tv/)|([^0-9A-Za-z \t])|LFT|lft", " ", match.group(1))
          if len(name1) == 0:
            name1 = match.group(1)
          steamID1 = match.group(3)
          team1 = match.group(4)
          name2 = re.sub("(@[A-Za-z0-9]+)|(twitch.tv/)|([^0-9A-Za-z \t])|LFT|lft", " ", match.group(5))
          if len(name2) == 0:
            name2 = match.group(5)
          steamID2 = match.group(7)
          team2 = match.group(8)
          weapon = match.group(9)
          if "customkill \"headshot\"" in line:
            weapon += "_headshot"
          elif "customkill \"backstab\"" in line:
            weapon += "_backstab"
          if team1 == "Red":
            team1 = 19
            team2 = 18
          else:
            team1 = 18
            team2 = 19
          self.Broadcast.broadcast(["log", "kill", [team1, name1], [team2, name2], weapon], matchID)

class LogsProtocol(DatagramProtocol):
  def __init__(self, Handler):
    self.Handler = Handler

  def datagramReceived(self, data, (ip, port)):
    data = data.decode("ascii", "ignore")
    if data[0] == "S":
      logsecret = re.search(r"^S(.*?)L", data).group(1)
      data = data[len(logsecret) + 3:]
    else:
      logsecret = False
      data = data[3:]
    self.Handler.logline("%s:%d" % (ip, port), logsecret, data)