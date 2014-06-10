# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1398068680.279277
_enable_loop = True
_template_filename = u'/repos/saloon.tf/Website/website/templates/manage/partials.mako'
_template_uri = u'/manage/teams/../partials.mako'
_source_encoding = 'utf-8'
from markupsafe import escape
_exports = [u'menu', u'dashboardBets', u'dashboardFixtures']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def menu():
            return render_menu(context._locals(__M_locals))
        c = context.get('c', UNDEFINED)
        def dashboardBets():
            return render_dashboardBets(context._locals(__M_locals))
        def dashboardFixtures():
            return render_dashboardFixtures(context._locals(__M_locals))
        __M_writer = context.writer()
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'menu'):
            context['self'].menu(**pageargs)
        

        # SOURCE LINE 14
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'dashboardBets'):
            context['self'].dashboardBets(**pageargs)
        

        # SOURCE LINE 24
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'dashboardFixtures'):
            context['self'].dashboardFixtures(**pageargs)
        

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_menu(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def menu():
            return render_menu(context)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n  <div class="col-sm-3">\n    <div class="list-group">\n      <a href="/manage/" class="list-group-item ')
        # SOURCE LINE 4
        __M_writer(escape('active' if c.managePage == "dashboard" else ''))
        __M_writer(u'">\n        <i class="fa fa-th-large"></i> Dashboard\n      </a>\n      <a href="/manage/leagues/" class="list-group-item ')
        # SOURCE LINE 7
        __M_writer(escape('active' if c.managePage == "leagues" else ''))
        __M_writer(u'"><i class="fa fa-trophy"></i> Leagues</a>\n      <a href="/manage/teams/" class="list-group-item ')
        # SOURCE LINE 8
        __M_writer(escape('active' if c.managePage == "teams" else ''))
        __M_writer(u'"><i class="fa fa-users"></i> Teams</a>\n      <a href="#" class="list-group-item"><i class="fa fa-gavel"></i> Matches</a>\n      <a href="#" class="list-group-item"><i class="fa fa-user"></i> Users</a>\n      <a href="#" class="list-group-item"><i class="fa fa-ticket"></i> Tickets</a>\n    </div>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_dashboardBets(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def dashboardBets():
            return render_dashboardBets(context)
        __M_writer = context.writer()
        # SOURCE LINE 15
        __M_writer(u'\n  <div class="col-sm-12">\n    <div class="panel panel-primary">\n      <div class="panel-heading"><i class="fa fa-bar-chart-o"></i> Bets</div>\n      <div class="panel-body">\n        <p>Placeholder for bets chart.</p>\n      </div>\n    </div>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_dashboardFixtures(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def dashboardFixtures():
            return render_dashboardFixtures(context)
        __M_writer = context.writer()
        # SOURCE LINE 25
        __M_writer(u'\n  <div class="col-sm-6">\n    <div class="panel panel-primary">\n      <div class="panel-heading"><i class="fa fa-list"></i> Fixtures</div>\n      <div class="panel-body">\n        <p>Placeholder for upcoming fixtures list.</p>\n      </div>\n    </div>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


