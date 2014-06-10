import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render
import database as db

log = logging.getLogger(__name__)

class TradeController(BaseController):

    def index(self, id):
        # Return a rendered template
        #return render('/trade.mako')
        # or, return a string
        RBot = db.Session.query(db.Bots).filter(db.Bots.id == id).first()
        if RBot and RBot.tradeLink:
          c.current = "trade"
          c.user = False
          c.url = RBot.tradeLink
          return render('/trade.mako')
        else:
          return redirect("http://saloon.tf/home/")