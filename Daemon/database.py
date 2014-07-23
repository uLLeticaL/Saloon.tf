from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Boolean, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import DateTime
from sqlalchemy.orm import mapper, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import or_

Base = declarative_base()

class Bots(Base):
  __tablename__ = "bots"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  emailAddress = Column(String)
  emailPassword = Column(String)
  steamLogin = Column(String)
  steamPassword = Column(String)
  steamAPI = Column(String)
  backpackAPI = Column(String)
  steamID = Column(String)
  tradeLink = Column(String)

class Users(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  name = Column(String(convert_unicode=True))
  avatar = Column(String)
  steamID = Column(Integer)
  bot = Column(Integer)
  token = Column(String)
  Permissions = relationship("UsersPermissions")

class UsersPermissions(Base):
  __tablename__ = "usersPermissions"
  user = Column(Integer, ForeignKey("users.id"), primary_key=True)
  manage = Column(Boolean)
  leagues = Column(Boolean)
  teams = Column(Boolean)
  users = Column(Boolean)
  bets = Column(Boolean)
  bots = Column(Boolean)
  permissions = Column(Boolean)

class Leagues(Base):
  __tablename__ = "leagues"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  type = Column(String)
  region = Column(String)
  colour = Column(String)

class Teams(Base):
  __tablename__ = "teams"
  id = Column(Integer, primary_key=True)
  name = Column(String(convert_unicode=True))
  country = Column(String, ForeignKey("countries.id"))
  Country = relationship("Countries")
  league = Column(Integer)
  leagueID = Column(Integer)

class Matches(Base):
  __tablename__ = "matches"
  id = Column(Integer, ForeignKey("betsTotal.match"), ForeignKey("streams.match"), primary_key=True)
  league = Column(Integer, ForeignKey("leagues.id"))
  League = relationship("Leagues")
  leaguesID = Column(Integer)
  team1 = Column(Integer, ForeignKey("teams.id"), ForeignKey("betsTotal.team"))
  Team1 = relationship("Teams", foreign_keys=team1)
  BetsTotal1 = relationship("BetsTotal", primaryjoin="and_(Matches.id == BetsTotal.match, Matches.team1 == BetsTotal.team)")
  team2 = Column(Integer, ForeignKey("teams.id"), ForeignKey("betsTotal.team"))
  Team2 = relationship("Teams", foreign_keys=team2)
  BetsTotal2 = relationship("BetsTotal", primaryjoin="and_(Matches.id == BetsTotal.match, Matches.team2 == BetsTotal.team)")
  status = Column(Integer, default = 0)
  time = Column(Integer, default = 0)
  points1 = Column(Integer, default = 0)
  points2 = Column(Integer, default = 0)
  Stream = relationship("Streams")

class Streams(Base):
  __tablename__ = "streams"
  id = Column(Integer, primary_key=True)
  match = Column(Integer)
  channel = Column(String)
  ip = Column(String)
  port = Column(Integer)
  rcon = Column(String)
  logsecret = Column(String)

class BetsTotal(Base):
  __tablename__ = "betsTotal"
  id = Column(Integer, primary_key=True)
  match = Column(Integer)
  team = Column(Integer)
  groups = Column(ARRAY(Integer))
  value = Column(Integer)

class Bets(Base):
  __tablename__ = "bets"
  id = Column(Integer, primary_key=True)
  user = Column(Integer, ForeignKey("users.id"))
  User = relationship("Users")
  match = Column(Integer)
  team = Column(Integer)
  groups = Column(ARRAY(Integer), default = [])
  items = Column(ARRAY(BigInteger), default = [])
  value = Column(Integer, default = 0)
  status = Column(Integer, default = 0)
  wonGroups = Column(ARRAY(Integer), default = [])
  wonItems = Column(ARRAY(BigInteger), default = [])
  offerID = Column(Integer)
  created = Column(DateTime)
  updated = Column(DateTime)

class BetsDetailed(Base):
  __tablename__ = "bets"
  __table_args__ = {"extend_existing": True}
  id = Column(Integer, primary_key=True)
  user = Column(Integer, ForeignKey("users.id"))
  User = relationship("Users")
  match = Column(Integer, ForeignKey("matches.id"))
  Match = relationship("Matches")
  team = Column(Integer, ForeignKey("teams.id"))
  Team = relationship("Teams")
  groups = Column(ARRAY(Integer), default = [])
  items = Column(ARRAY(BigInteger), default = [])
  value = Column(Integer, default = 0)
  wonGroups = Column(ARRAY(Integer), default = [])
  wonItems = Column(ARRAY(BigInteger), default = [])
  offerID = Column(Integer)
  created = Column(DateTime)
  updated = Column(DateTime)

class Items(Base):
  __tablename__ = "items"
  id = Column(Integer, primary_key=True)
  description = Column(String)
  defindex = Column(Integer)
  value = Column(Integer)
  type = Column(Integer)
  quality = Column(Integer)
  timestamp = Column(Integer)

class Countries(Base):
  __tablename__ = "countries"
  id = Column(String, primary_key=True)
  name = Column(String)

from sqlalchemy import create_engine
engine = create_engine("postgresql://postgres:password@localhost:5432/Saloon.tf", echo = False, echo_pool = False, isolation_level="READ UNCOMMITTED")

Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
Session = DBSession()
