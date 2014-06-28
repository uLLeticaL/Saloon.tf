import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render
from sqlalchemy import func
import database as db
import json

log = logging.getLogger(__name__)

class ApiController(BaseController):

  def users(self, name = False, steamid = False, limit = False):
    # Return a json string
    if limit:
      limit = int(limit)
      if limit > 10:
        limit = 10
    print limit
    if name:
      name = name.lower()
      RUsers = db.Session.query(db.Users).filter(func.lower(db.Users.name).like(name + "%")).limit(limit).all()
    else:
      RUsers = db.Session.query(db.Users).filter(db.Users.steamid == steamid).limit(limit).all()

    users = []
    for RUser in RUsers:
      user = {}
      user["id"] = RUser.id
      user["name"] = RUser.name
      user["steamid"] = RUser.steamID
      users.append(user)

    return json.dumps(users)
