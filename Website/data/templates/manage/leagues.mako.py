# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1398113986.967148
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/manage/leagues.mako'
_template_uri = '/manage/leagues.mako'
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
    # SOURCE LINE 141
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
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="modal fade" id="removeLeague-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-times-circle"></i> Remove</h3>\n      </div>\n      <div class="modal-body">\n        <p>Are you sure you want to delete this league?</p>\n        <div class="btn-group">\n          <button id="removeLeague-confirm" class="btn btn-primary">Yes</button>\n          <button data-dismiss="modal" aria-hidden="true" class="btn btn-primary float-right">No</button>\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="modal fade" id="addLeague-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-plus-circle"></i> Add</h3>\n      </div>\n      <div class="modal-body">\n        <form role="form" id="addLeague-form" method="POST" action="/manage/leagues/add/" enctype="multipart/form-data">\n          <div class="form-group">\n            <label for="name">Name</label>\n            <input type="text" class="form-control" name="name" placeholder="Enter name">\n          </div>\n          <p>Type<br>\n          <div class="btn-group" data-toggle="buttons">\n            <label class="btn btn-primary">\n              <input type="radio" name="type" value="6on6"> 6on6\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="type" value="Highlander"> Highlander\n            </label>\n          </div>\n          </p>\n          <p>Region<br>\n          <div class="btn-group" data-toggle="buttons">\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="North America"> North America\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="South America"> South America\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="Europe"> Europe\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="Asia"> Asia\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="Australia and Oceania"> Australia and Oceania\n            </label>\n          </div>\n          </p>\n          <p>Avatar</p>\n          <div class="fileinput fileinput-new input-group" data-provides="fileinput">\n            <div class="form-control fileinput-control" data-trigger="fileinput">\n              <i class="fa fa-file"></i> <span class="fileinput-filename"></span>\n            </div>\n            <span class="input-group-addon btn btn-default btn-file">\n              <span class="fileinput-new">Select file</span>\n              <span class="fileinput-exists">Change</span>\n              <input type="file" name="avatar">\n            </span>\n            <a href="#" class="input-group-addon btn btn-default fileinput-exists" data-dismiss="fileinput">Remove</a>\n          </div>\n          <div class="form-group">\n            <label for="accentColour">Colour</label>\n            <input type="text" class="form-control" name="accentColour" id="accentColour" placeholder="222222">\n          </div>\n          <button type="submit" class="btn btn-primary">Submit</button>\n        </form>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="modal fade" id="editLeague-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-pencil"></i> Edit</h3>\n      </div>\n      <div class="modal-body">\n        <form role="form" id="editLeague-form">\n          <div class="form-group">\n            <label for="name">Name</label>\n            <input type="text" class="form-control" name="name" placeholder="Enter name">\n          </div>\n          <p>Type<br>\n          <div class="btn-group" data-toggle="buttons">\n            <label class="btn btn-primary">\n              <input type="radio" name="type" value="6on6"> 6on6\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="type" value="Highlander"> Highlander\n            </label>\n          </div>\n          </p>\n          <p>Region<br>\n          <div class="btn-group" data-toggle="buttons">\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="North America"> North America\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="South America"> South America\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="Europe"> Europe\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="Asia"> Asia\n            </label>\n            <label class="btn btn-primary">\n              <input type="radio" name="region" value="Australia and Oceania"> Australia and Oceania\n            </label>\n          </div>\n          </p>\n          <div class="form-group">\n            <label for="accentColour">Colour</label>\n            <input type="text" class="form-control" name="accentColour" id="accentColour" placeholder="222222">\n          </div>\n          <button type="submit" class="btn btn-primary">Submit</button>\n        </form>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="container manage">\n  <div class="row">\n    ')
        # SOURCE LINE 141
        __M_writer(u'\n    ')
        # SOURCE LINE 142
        __M_writer(escape(partials.menu()))
        __M_writer(u'\n    <div class="col-sm-9">\n      <div class="header">\n        <h2><i class="fa fa-trophy"></i> Leagues</h2>\n        <div class="button-panel pull-right">\n          <button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#addLeague-modal"><i class="fa fa-plus-circle"></i> Add</button>\n        </div>\n      </div>\n')
        # SOURCE LINE 150
        for league in c.leagues:
            # SOURCE LINE 151
            __M_writer(u'        <div class="well league ')
            __M_writer(escape(league["name"]))
            __M_writer(u'">\n          <div class="league-badge" style="background-color: #')
            # SOURCE LINE 152
            __M_writer(escape(league["colour"]))
            __M_writer(u';">\n            <img src="/images/leagues/')
            # SOURCE LINE 153
            __M_writer(escape(league["id"]))
            __M_writer(u'/logo.png">\n          </div>\n          <div class="details">\n            <h3><i class="fa fa-trophy"></i> ')
            # SOURCE LINE 156
            __M_writer(escape(league["name"]))
            __M_writer(u'</h3>\n            <h3><i class="fa fa-globe"></i> ')
            # SOURCE LINE 157
            __M_writer(escape(league["region"]))
            __M_writer(u'</h3>\n            <h3><i class="fa fa-flag"></i> ')
            # SOURCE LINE 158
            __M_writer(escape(league["type"]))
            __M_writer(u'</h3>\n          </div>\n          <div class="pull-right">\n            <div class="btn-group btn-block">\n              <button class="btn btn-md btn-primary editLeague-button" data-json=\'')
            # SOURCE LINE 162
            __M_writer(escape(league["json"]))
            __M_writer(u'\'><i class="fa fa-pencil"></i> Edit</button>\n              <button class="btn btn-md btn-primary removeLeague-button" data-id="')
            # SOURCE LINE 163
            __M_writer(escape(league["id"]))
            __M_writer(u'"><i class="fa fa-times-circle"></i> Remove</button>\n            </div>\n          </div>\n        </div>\n')
        # SOURCE LINE 168
        __M_writer(u'    </div>\n  </div>\n</div>')
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


