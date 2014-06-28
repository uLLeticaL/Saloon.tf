import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render
from website.model.user import User
import database as db

log = logging.getLogger(__name__)

class InventoryController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/inventory.mako')
        # or, return a string
        user = User()
        if user:
            RUser = user[0]
            c.user = user[1]
            c.current = "inventory"
            if not c.user:
              return redirect("http://saloon.tf/home/")
            c.inventory = {}
            c.inventory["names"] = ["keys","refs","recs","scraps"]
            c.hasItems = False
            c.inventory["quantity"] = []
            c.inventory["quantity"].append(c.user["items"].keys)
            if c.user["items"].keys > 0 or c.user["items"].metal > 0:
                c.hasItems = True
            metal = c.user["items"].metal
            c.inventory["quantity"].append(metal / 9)
            metal -= c.inventory["quantity"][1] * 9
            c.inventory["quantity"].append(metal / 3)
            metal -= c.inventory["quantity"][2] * 3
            c.inventory["quantity"].append(metal)
            return render('/inventory.mako')
        else:
            return redirect('http://saloon.tf/home/')