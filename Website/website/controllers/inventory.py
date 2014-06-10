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
            c.items = {}
            c.items["names"] = ["keys","refs","recs","scraps"]
            c.hasItems = False
            c.items["quantity"] = []
            c.items["quantity"].append(RUser.Items[0].keys)
            if RUser.Items[0].keys > 0:
                c.hasItems = True
            metal = RUser.Items[0].metal
            if metal > 0:
                c.hasItems = True
            c.items["quantity"].append(metal / 9)
            metal -= c.items["quantity"][1] * 9
            c.items["quantity"].append(metal / 3)
            metal -= c.items["quantity"][2] * 3
            c.items["quantity"].append(metal)
            return render('/inventory.mako')
        else:
            return redirect('http://saloon.tf/home/')