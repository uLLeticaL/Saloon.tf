import logging
import requests
import re

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/login.mako')
        # or, return a string
        if "steamid" in session:
          return redirect("http://saloon.tf/home/")

        if request.GET.get('openid.signed'):
          params = {
            'openid.assoc_handle': request.GET.get("openid.assoc_handle"),
            'openid.signed': request.GET.get("openid.signed"),
            'openid.sig': request.GET.get("openid.sig"),
            'openid.ns': 'http://specs.openid.net/auth/2.0',
          }
          signed = request.GET.get('openid.signed').split(",")
          for item in signed:
              params['openid.' + item] = request.GET.get('openid.' + item.replace(".", "_"))
          params['openid.mode'] = 'check_authentication'
          data = requests.post('https://steamcommunity.com/openid/login', params=params).text
          if data == "ns:http://specs.openid.net/auth/2.0\nis_valid:true\n":
            claimedID = request.GET.get('openid.claimed_id')
            steamID = claimedID = claimedID[36:]
            session["steamid"] = int(steamID)
            session.save()
            return redirect("/home/")
        return redirect("https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=http%3A%2F%2Fstaging.saloon.tf%2Flogin&openid.realm=http%3A%2F%2Fsaloon.tf&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select")