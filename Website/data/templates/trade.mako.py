# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1403610087.537615
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/trade.mako'
_template_uri = '/trade.mako'
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
        # SOURCE LINE 7
        __M_writer(u'\n\n<div class="container">\n  <div class="well">\n    <p><i class="fa fa-exclamation-triangle"></i> You must have pop ups enabled to send the trade offer.</p>\n  </div>\n</div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n  <script type="text/javascript">\n    window.open( "')
        # SOURCE LINE 5
        __M_writer(c.url )
        __M_writer(u'", "_self" );\n  </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


