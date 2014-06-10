# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1397824712.176635
_enable_loop = True
_template_filename = u'/repos/saloon.tf/Website/website/templates/manage/base.mako'
_template_uri = u'/manage/base.mako'
_source_encoding = 'utf-8'
from markupsafe import escape
_exports = [u'header', 'head_tags']


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
        def header():
            return render_header(context._locals(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="container manage">\n  <div class="manage-header">\n    <h2><i class="fa fa-wrench"></i> Manage</h2>\n  </div>\n  <div class="row">\n    <div class="col-sm-3">\n      <div class="list-group">\n        <a href="#" class="list-group-item active">\n          <i class="fa fa-tachometer"></i> Dashboard\n        </a>\n        <a href="#" class="list-group-item"><i class="fa fa-trophy"></i> Leagues</a>\n        <a href="#" class="list-group-item"><i class="fa fa-users"></i> Teams</a>\n        <a href="#" class="list-group-item"><i class="fa fa-gavel"></i> Matches</a>\n        <a href="#" class="list-group-item"><i class="fa fa-user"></i> Users</a>\n        <a href="#" class="list-group-item"><i class="fa fa-ticket"></i> Tickets</a>\n      </div>\n    </div>\n    <div class="col-sm-9">\n      ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        # SOURCE LINE 24
        __M_writer(u'\n    </div>\n  </div>\n</div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def header():
            return render_header(context)
        __M_writer = context.writer()
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


