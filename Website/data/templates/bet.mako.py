# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1403562628.65853
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/bet.mako'
_template_uri = '/bet.mako'
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
        __M_writer(u'\n<div class="container bets">\n  <div class="well bet ')
        # SOURCE LINE 7
        __M_writer(escape(c.match["league"]["name"]))
        __M_writer(u' text-center" data-id="')
        __M_writer(escape(c.match["id"]))
        __M_writer(u'">\n    <div class="league-badge" style="background-color: #')
        # SOURCE LINE 8
        __M_writer(escape(c.match["league"]["colour"]))
        __M_writer(u';">\n      <img src="/images/leagues/')
        # SOURCE LINE 9
        __M_writer(escape(c.match["league"]["id"]))
        __M_writer(u'/logo.png">\n    </div>\n')
        # SOURCE LINE 11
        for id, team in enumerate(c.match["teams"]):
            # SOURCE LINE 12
            __M_writer(u'      <div class="team-')
            __M_writer(escape(id))
            __M_writer(u'">\n')
            # SOURCE LINE 13
            if id is 0:
                # SOURCE LINE 14
                __M_writer(u'          <img src="/images/teams/')
                __M_writer(escape(team["id"]))
                __M_writer(u'.jpg">\n')
            # SOURCE LINE 16
            __M_writer(u'        <div class="details">\n          <h2>')
            # SOURCE LINE 17
            __M_writer(escape(team["name"]))
            __M_writer(u'</h2>\n          <span class="specifics">\n            <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n            <p><i class="fa fa-thumbs-up"></i> ')
            # SOURCE LINE 20
            __M_writer(escape(team["bets"]["percentage"]))
            __M_writer(u'%</p>\n          </span>\n        </div>\n')
            # SOURCE LINE 23
            if id is 1:
                # SOURCE LINE 24
                __M_writer(u'            <img src="/images/teams/')
                __M_writer(escape(team["id"]))
                __M_writer(u'.jpg">\n')
            # SOURCE LINE 26
            __M_writer(u'      </div>\n')
        # SOURCE LINE 28
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


