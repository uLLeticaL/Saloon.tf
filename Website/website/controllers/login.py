import logging
import urllib
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
          parameters = {
            'openid.assoc_handle': request.GET.get("openid.assoc_handle"),
            'openid.signed': request.GET.get("openid.signed"),
            'openid.sig': request.GET.get("openid.sig"),
            'openid.ns': 'http://specs.openid.net/auth/2.0',
          }
          signed = request.GET.get('openid.signed').split(",")
          for item in signed:
              parameters['openid.' + item] = request.GET.get('openid.' + item.replace(".", "_"))
          parameters['openid.mode'] = 'check_authentication'
          data = requests.post('https://steamcommunity.com/openid/login', params=parameters).text
          if data == "ns:http://specs.openid.net/auth/2.0\nis_valid:true\n":
            claimedID = request.GET.get('openid.claimed_id')
            steamID = claimedID = claimedID[36:]
            session["steamid"] = int(steamID)
            session.save()
            return redirect("/home/")
        parameters = {
          "openid.ns": "http://specs.openid.net/auth/2.0",
          "openid.mode": "checkid_setup",
          "openid.return_to": "http://%s/login" % (request.headers["Host"]),
          "openid.realm": "http://%s" % (request.headers["Host"]),
          "openid.ns.sreg": "http://openid.net/extensions/sreg/1.1",
          "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
          "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        }
        data = urllib.urlencode(parameters)
        return redirect("https://steamcommunity.com/openid/login/?" + data)