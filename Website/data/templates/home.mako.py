# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1398111533.249799
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/home.mako'
_template_uri = '/home.mako'
_source_encoding = 'utf-8'
from markupsafe import escape
_exports = ['head_tags']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="container bets">\n  <div class="header">\n    <h2><i class="fa fa-gavel"></i> Bets</h2>\n  </div>\n')
        # SOURCE LINE 10
        for match in c.matches:
            # SOURCE LINE 11
            __M_writer(u'    <div class="well bet ')
            __M_writer(escape(match["league"]["name"]))
            __M_writer(u' text-center" data-id="')
            __M_writer(escape(match["id"]))
            __M_writer(u'">\n      <div class="league-badge" style="background-color: #')
            # SOURCE LINE 12
            __M_writer(escape(match["league"]["colour"]))
            __M_writer(u';">\n        <img src="/images/leagues/')
            # SOURCE LINE 13
            __M_writer(escape(match["league"]["id"]))
            __M_writer(u'/logo.png">\n      </div>\n')
            # SOURCE LINE 15
            for id, team in enumerate(match["teams"]):
                # SOURCE LINE 16
                __M_writer(u'        <div class="team-')
                __M_writer(escape(id))
                __M_writer(u'">\n')
                # SOURCE LINE 17
                if id is 0:
                    # SOURCE LINE 18
                    __M_writer(u'            <img src="/images/teams/')
                    __M_writer(escape(team["id"]))
                    __M_writer(u'.jpg">\n')
                # SOURCE LINE 20
                __M_writer(u'          <div class="details">\n            <h3>')
                # SOURCE LINE 21
                __M_writer(escape(team["name"]))
                __M_writer(u'</h3>\n            <span class="specifics">\n              <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n              <p><i class="fa fa-thumbs-up"></i> ')
                # SOURCE LINE 24
                __M_writer(escape(team["bets"]["percentage"]))
                __M_writer(u'%</p>\n            </span>\n          </div>\n')
                # SOURCE LINE 27
                if id is 1:
                    # SOURCE LINE 28
                    __M_writer(u'            <img src="/images/teams/')
                    __M_writer(escape(team["id"]))
                    __M_writer(u'.jpg">\n')
                # SOURCE LINE 30
                __M_writer(u'        </div>\n')
            # SOURCE LINE 32
            __M_writer(u'    </div>\n')
        # SOURCE LINE 34
        __M_writer(u'</div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n  <!-- add some head tags here -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


