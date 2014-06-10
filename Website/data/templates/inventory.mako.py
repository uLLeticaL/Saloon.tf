# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1398111705.439354
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/inventory.mako'
_template_uri = '/inventory.mako'
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
        range = context.get('range', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="modal fade" id="deposit-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-sign-in"></i> Deposit</h3>\n      </div>\n      <div class="modal-body">\n        <p class="connection-status"><i class="fa fa-spinner fa-spin"></i> Establishing connection with bot</p>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="modal fade" id="withdraw-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-sign-out"></i> Withdraw</h3>\n      </div>\n      <div class="modal-body">\n        <p class="connection-status"><i class="fa fa-spinner fa-spin"></i> Establishing connection with bot</p>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="container">\n  <div class="header">\n    <h2><i class="fa fa-briefcase"></i> Inventory</h2>\n    <div class="button-panel pull-right">\n      <button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#deposit-modal"><i class="fa fa-sign-in"></i> Deposit</button>\n      <button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#withdraw-modal"><i class="fa fa-sign-out"></i> Withdraw</button>\n      <button class="btn btn-lg btn-primary"><i class="fa fa-gavel"></i> Bet</button>\n    </div>\n  </div>\n  <div class="items well">\n')
        # SOURCE LINE 42
        if c.hasItems:
            # SOURCE LINE 43
            for index, name in enumerate(c.items["names"]):
                # SOURCE LINE 44
                for item in range(0, c.items["quantity"][index]):
                    # SOURCE LINE 45
                    __M_writer(u'          <div class="item ')
                    __M_writer(escape(name))
                    __M_writer(u'">\n            <div class="check"><i class="fa fa-check"></i></div>\n            <img src="/images/items/')
                    # SOURCE LINE 47
                    __M_writer(escape(name))
                    __M_writer(u'.png">\n          </div>\n')
            # SOURCE LINE 51
        else:
            # SOURCE LINE 52
            __M_writer(u'      <p class="text-center">You don\'t have any items yet.<br>Please deposit some before you start betting.</p>\n      <p class="text-center"><button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#deposit-modal"><i class="fa fa-sign-in"></i> Deposit</button></p>\n')
        # SOURCE LINE 55
        __M_writer(u'  </div>\n</div>')
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


