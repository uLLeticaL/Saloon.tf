# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1403610349.685381
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/manage/teams/index.mako'
_template_uri = '/manage/teams/index.mako'
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
    # SOURCE LINE 8
    ns = runtime.TemplateNamespace(u'partials', context._clean_inheritance_tokens(), templateuri=u'../partials.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'partials')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        partials = _mako_get_namespace(context, 'partials')
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="container manage">\n  <div class="row">\n    ')
        # SOURCE LINE 8
        __M_writer(u'\n    ')
        # SOURCE LINE 9
        __M_writer(escape(partials.menu()))
        __M_writer(u'\n    <div class="col-sm-9">\n      <div class="header">\n        <h2><i class="fa fa-users"></i> Teams</h2>\n        <h3><i class="fa fa-filter"></i> Filters</h3>\n      </div>\n      <div class="well">\n')
        # SOURCE LINE 16
        for league in c.leagues:
            # SOURCE LINE 17
            __M_writer(u'          <a href="/manage/teams/')
            __M_writer(escape(league["id"]))
            __M_writer(u'/">\n            <span class="league-block ')
            # SOURCE LINE 18
            __M_writer(escape(league["name"]))
            __M_writer(u'">\n              <div class="league-badge" style="background-color: #')
            # SOURCE LINE 19
            __M_writer(escape(league["colour"]))
            __M_writer(u';">\n                <img src="/images/leagues/')
            # SOURCE LINE 20
            __M_writer(escape(league["id"]))
            __M_writer(u'/logo.png">\n              </div>\n              <div class="details-overlay">\n                <h3><i class="fa fa-globe"></i> ')
            # SOURCE LINE 23
            __M_writer(escape(league["region"]))
            __M_writer(u'</h3>\n                <h3><i class="fa fa-flag"></i> ')
            # SOURCE LINE 24
            __M_writer(escape(league["type"]))
            __M_writer(u'</h3>\n              </div>\n            </span>\n          </a>\n')
        # SOURCE LINE 29
        __M_writer(u'      </div>\n    </div>\n  </div>\n</div>')
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


