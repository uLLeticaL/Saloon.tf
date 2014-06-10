# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1397240681.876977
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/placeholder.mako'
_template_uri = '/placeholder.mako'
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
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="container bets">\n  <div class="well bet etf2l text-center">\n    <div class="league">\n      <img src="/images/leagues/etf2l/etf2llogo.png">\n    </div>\n    <div class="team-0">\n      <img src="/images/leagues/etf2l/fenneks.jpg">\n      <div class="details">\n        <h2>Fenneks eSports</h2>\n        <span class="specifics">\n          <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n          <p><i class="fa fa-thumbs-up"></i> 53%</p>\n        </span>\n      </div>\n    </div>\n    <div class="team-1">\n      <div class="details">\n        <h2>The Last Resort</h2>\n        <span class="specifics">\n          <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n          <p><i class="fa fa-thumbs-down"></i> 47%</p>\n        </span>\n      </div>\n      <img src="/images/leagues/etf2l/tlr.jpg">\n    </div>\n  </div>\n  <div class="well bet cevo text-center">\n    <div class="league">\n      <img src="/images/leagues/cevo/cevologo.png">\n    </div>\n    <div class="team-0">\n      <img src="/images/leagues/cevo/froyotech.jpg">\n      <div class="details">\n        <h2>FROYOTech</h2>\n        <span class="specifics">\n          <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n          <p><i class="fa fa-thumbs-up"></i> 87%</p>\n        </span>\n      </div>\n    </div>\n    <div class="team-1">\n      <div class="details">\n        <h2>Xero Error</h2>\n        <span class="specifics">\n          <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n          <p><i class="fa fa-thumbs-down"></i> 13%</p>\n        </span>\n      </div>\n      <img src="/images/leagues/cevo/xeroerrorgamingtf2.jpg">\n    </div>\n  </div>\n  <div class="well bet ugc text-center">\n    <div class="league">\n      <img src="/images/leagues/ugc/ugclogo.png">\n    </div>\n    <div class="team-0">\n      <img src="/images/leagues/ugc/dunning-krugereffect.jpg">\n      <div class="details">\n        <h2>Dunning-Kruger Effect</h2>\n        <span class="specifics">\n          <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n          <p><i class="fa fa-thumbs-up"></i> 98%</p>\n        </span>\n      </div>\n    </div>\n    <div class="team-1">\n      <div class="details">\n        <h2>Sinful Six</h2>\n        <span class="specifics">\n          <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>\n          <p><i class="fa fa-thumbs-down"></i> 2%&nbsp;</p>\n        </span>\n      </div>\n      <img src="/images/leagues/ugc/sinfulsix.jpg">\n    </div>\n  </div>\n</div>')
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


