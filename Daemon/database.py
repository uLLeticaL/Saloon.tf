import settings
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import mapper, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import or_

Base = declarative_base()

class Bots(Base):
  __tablename__ = 'bots'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  emailAddress = Column(String)
  emailPassword = Column(String)
  steamLogin = Column(String)
  steamPassword = Column(String)
  steamAPI = Column(String)
  steamID = Column(String)
  tradeLink = Column(String)

class Users(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(convert_unicode=True))
  avatar = Column(String)
  steamID = Column(Integer)
  bot = Column(Integer)
  Items = relationship("UsersItems")
  Permissions = relationship("UsersPermissions")

class UsersItems(Base):
  __tablename__ = 'usersItems'
  user = Column(Integer, ForeignKey('users.id'), primary_key=True)
  keys = Column(Integer)
  metal = Column(Integer)

class UsersPermissions(Base):
  __tablename__ = 'usersPermissions'
  user = Column(Integer, ForeignKey('users.id'), primary_key=True)
  manage = Column(Boolean)
  leagues = Column(Boolean)
  teams = Column(Boolean)
  users = Column(Boolean)
  bets = Column(Boolean)
  bots = Column(Boolean)

class Matches(Base):
  __tablename__ = 'matches'
  id = Column(Integer, primary_key=True)
  league = Column(Integer, ForeignKey('leagues.id'))
  team1 = Column(Integer, ForeignKey('teams.id'), ForeignKey('betsTotal.team'))
  team2 = Column(Integer, ForeignKey('teams.id'), ForeignKey('betsTotal.team'))
  stream = Column(String)
  won = Column(Integer)
  League = relationship("Leagues")
  Team1 = relationship("Teams", foreign_keys=team1)
  Team2 = relationship("Teams", foreign_keys=team2)
  BetsTotal1 = relationship("BetsTotal", foreign_keys=team1)
  BetsTotal2 = relationship("BetsTotal", foreign_keys=team2)

class Leagues(Base):
  __tablename__ = 'leagues'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  type = Column(String)
  region = Column(String)
  colour = Column(String)

class Teams(Base):
  __tablename__ = 'teams'
  id = Column(Integer, primary_key=True)
  name = Column(String(convert_unicode=True))
  country = Column(String, ForeignKey('countries.id'))
  Country = relationship("Countries")
  league = Column(Integer)
  leagueID = Column(Integer)

class BetsTotal(Base):
  __tablename__ = "betsTotal"
  id = Column(Integer, primary_key=True)
  match = Column(Integer)
  team = Column(Integer)
  buds = Column(String)
  bills = Column(Integer)
  keys = Column(Integer)
  metal = Column(Integer)

class Items(Base):
  __tablename__ = "items"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  metal = Column(Boolean)
  defindex = Column(Integer)
  assetID = Column(Integer)
  classID = Column(Integer)
  value = Column(Integer)

class Countries(Base):
  __tablename__ = 'countries'
  id = Column(String, primary_key=True)
  name = Column(String)

from sqlalchemy import create_engine
engine = create_engine(settings.database, echo = False, echo_pool = False, isolation_level="READ UNCOMMITTED")

Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
Session = DBSession()