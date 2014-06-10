# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1398594533.388445
_enable_loop = True
_template_filename = u'/repos/saloon.tf/Website/website/templates/base.mako'
_template_uri = u'/base.mako'
_source_encoding = 'utf-8'
from markupsafe import escape
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html>\n<html>\n  <head>\n    ')
        # SOURCE LINE 4
        __M_writer(escape(self.head_tags()))
        __M_writer(u'\n    <script type="text/javascript">\n      var page = "')
        # SOURCE LINE 6
        __M_writer(escape(c.current))
        __M_writer(u'";\n')
        # SOURCE LINE 7
        if c.user:
            # SOURCE LINE 8
            __M_writer(u'        var steamID = "')
            __M_writer(escape(c.user["steamid"]))
            __M_writer(u'";\n')
        # SOURCE LINE 10
        __M_writer(u'    </script>\n    <link href=\'http://fonts.googleapis.com/css?family=Lato:400,700\' rel=\'stylesheet\' type=\'text/css\'>\n    <link rel="stylesheet" type="text/css" href="/stylesheet.css" />\n  </head>\n  <body class="')
        # SOURCE LINE 14
        __M_writer(escape(c.current))
        __M_writer(u'">\n    <header>\n        <img src="/images/logo.png">\n    </header>\n    <nav class="navbar navbar-default" role="navigation">\n      <div class="container">\n        <div class="navbar-header">\n          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#top-navbar-collapse">\n            <span class="sr-only">Toggle navigation</span>\n            <span class="icon-bar"></span>\n            <span class="icon-bar"></span>\n            <span class="icon-bar"></span>\n          </button>\n        </div>\n        <div class="collapse navbar-collapse" id="top-navbar-collapse">\n          <ul class="nav navbar-nav">\n            <li class="')
        # SOURCE LINE 30
        __M_writer(escape('active' if c.current == "home" else ''))
        __M_writer(u'"><a href="/home/">Home</a></li>\n')
        # SOURCE LINE 31
        if c.user:
            # SOURCE LINE 32
            __M_writer(u'              <li class="')
            __M_writer(escape('active' if c.current == "inventory" else ''))
            __M_writer(u'"><a href="/inventory/">Inventory</a></li>\n')
            # SOURCE LINE 33
            if c.user["level"] <= 3:
                # SOURCE LINE 34
                __M_writer(u'                <li class="')
                __M_writer(escape('active' if c.current == "manage" else ''))
                __M_writer(u'"><a href="/manage/">Manage</a></li>\n')
        # SOURCE LINE 37
        __M_writer(u'          </ul>\n          <ul class="nav navbar-nav navbar-right">\n')
        # SOURCE LINE 39
        if c.user:
            # SOURCE LINE 40
            __M_writer(u'              <li><a href="/logout/">')
            __M_writer(escape(c.user["name"]))
            __M_writer(u'</a></li>\n')
            # SOURCE LINE 41
        else:
            # SOURCE LINE 42
            __M_writer(u'              <li><a href="/login/">Login</a></li>\n')
        # SOURCE LINE 44
        __M_writer(u'          </ul>\n        </div><!-- /.navbar-collapse -->\n      </div><!-- /.container-fluid -->\n    </nav>\n    ')
        # SOURCE LINE 48
        __M_writer(escape(self.body()))
        __M_writer(u'\n    <script type="text/javascript" src="/javascript.js?v=286" /></script>\n  </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


