# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1398113937.833071
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/manage/dashboard.mako'
_template_uri = '/manage/dashboard.mako'
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
    ns = runtime.TemplateNamespace(u'partials', context._clean_inheritance_tokens(), templateuri=u'partials.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'partials')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        partials = _mako_get_namespace(context, 'partials')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="container manage">\n  <div class="row">\n    ')
        # SOURCE LINE 8
        __M_writer(u'\n    ')
        # SOURCE LINE 9
        __M_writer(escape(partials.menu()))
        __M_writer(u'\n    <div class="col-sm-9">\n      <div class="header">\n        <h2><i class="fa fa-th-large"></i> Dashboard</h2>\n        <div class="button-panel pull-right">\n          <button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#addLeague-modal"><i class="fa fa-refresh"></i> Refresh</button>\n        </div>\n      </div>\n      <div class="row">\n        ')
        # SOURCE LINE 18
        __M_writer(escape(partials.dashboardBets()))
        __M_writer(u'\n        ')
        # SOURCE LINE 19
        __M_writer(escape(partials.dashboardFixtures()))
        __M_writer(u'\n        ')
        # SOURCE LINE 20
        __M_writer(escape(partials.dashboardFixtures()))
        __M_writer(u'\n      </div>\n    </div>\n  </div>\n</div>')
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


