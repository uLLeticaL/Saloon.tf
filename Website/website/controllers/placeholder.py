import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from website.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PlaceholderController(BaseController):

  def index(self):
    return render('/placeholder.mako')