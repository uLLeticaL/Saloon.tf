import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render

log = logging.getLogger(__name__)

class LogoutController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/logout.mako')
        # or, return a string
        session.delete()
        return redirect("http://saloon.tf/home/")
