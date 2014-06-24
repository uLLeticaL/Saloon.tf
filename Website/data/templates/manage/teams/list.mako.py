# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1403610406.32631
_enable_loop = True
_template_filename = '/repos/saloon.tf/Website/website/templates/manage/teams/list.mako'
_template_uri = '/manage/teams/list.mako'
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
    # SOURCE LINE 99
    ns = runtime.TemplateNamespace(u'partials', context._clean_inheritance_tokens(), templateuri=u'../partials.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'partials')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        partials = _mako_get_namespace(context, 'partials')
        enumerate = context.get('enumerate', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n<div class="modal fade" id="removeTeam-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-times-circle"></i> Remove</h3>\n      </div>\n      <div class="modal-body">\n        <p>Are you sure you want to delete this team?</p>\n        <div class="btn-group">\n          <button id="removeTeam-confirm" class="btn btn-primary">Yes</button>\n          <button data-dismiss="modal" aria-hidden="true" class="btn btn-primary float-right">No</button>\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="modal fade" id="addTeam-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-plus-circle"></i> Add</h3>\n      </div>\n      <div class="modal-body">\n        <form role="form" id="addTeam-form" method="POST" action="/manage/teams/')
        # SOURCE LINE 31
        __M_writer(escape(c.league["id"]))
        __M_writer(u'/add/" enctype="multipart/form-data">\n          <div class="form-group">\n            <label for="name">Name</label>\n            <input type="text" class="form-control" name="name" placeholder="Enter name">\n          </div>\n          <p>\n            Country<br>\n            <select name="country" class="form-control">\n')
        # SOURCE LINE 39
        for country in c.countries:
            # SOURCE LINE 40
            __M_writer(u'                <option value="')
            __M_writer(escape(country["id"]))
            __M_writer(u'">')
            __M_writer(escape(country["name"]))
            __M_writer(u'</option>\n')
        # SOURCE LINE 42
        __M_writer(u'            </select>\n          </p>\n          Avatar<br>\n          <div class="fileinput fileinput-new input-group" data-provides="fileinput">\n            <div class="form-control fileinput-control" data-trigger="fileinput">\n              <i class="fa fa-file"></i> <span class="fileinput-filename"></span>\n            </div>\n            <span class="input-group-addon btn btn-default btn-file">\n              <span class="fileinput-new">Select file</span>\n              <span class="fileinput-exists">Change</span>\n              <input type="file" name="avatar">\n            </span>\n            <a href="#" class="input-group-addon btn btn-default fileinput-exists" data-dismiss="fileinput">Remove</a>\n          </div>\n          <div class="form-group">\n            <label for="name">LeagueID</label>\n            <input type="text" class="form-control" name="leagueID" placeholder="Enter LeagueID">\n          </div>\n          <button type="submit" class="btn btn-primary">Submit</button>\n        </form>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="modal fade" id="editTeam-modal">\n  <div class="modal-dialog">\n    <div class="modal-content">\n      <div class="modal-header">\n        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n        <h3 class="modal-title"><i class="fa fa-pencil"></i> Edit</h3>\n      </div>\n      <div class="modal-body">\n        <form role="form" id="editTeam-form">\n          <div class="form-group">\n            <label for="name">Name</label>\n            <input type="text" class="form-control" name="name" placeholder="Enter name">\n          </div>\n          <p>\n            Country<br>\n            <select name="country" class="form-control">\n')
        # SOURCE LINE 82
        for country in c.countries:
            # SOURCE LINE 83
            __M_writer(u'                <option value="')
            __M_writer(escape(country["id"]))
            __M_writer(u'">')
            __M_writer(escape(country["name"]))
            __M_writer(u'</option>\n')
        # SOURCE LINE 85
        __M_writer(u'            </select>\n          </p>\n          <div class="form-group">\n            <label for="name">LeagueID</label>\n            <input type="text" class="form-control" name="leagueID" placeholder="Enter LeagueID">\n          </div>\n          <button type="submit" class="btn btn-primary">Submit</button>\n        </form>\n      </div>\n    </div>\n  </div>\n</div>\n<div class="container manage">\n  <div class="row">\n    ')
        # SOURCE LINE 99
        __M_writer(u'\n    ')
        # SOURCE LINE 100
        __M_writer(escape(partials.menu()))
        __M_writer(u'\n    <div class="col-sm-9">\n      <div class="header">\n        <h2><i class="fa fa-users"></i> Teams</h2>\n        <div class="button-panel pull-right">\n          <a href="/manage/teams/" class="btn btn-lg btn-primary"><i class="fa fa-reply"></i> Back</a>\n          <a class="btn btn-lg btn-primary" data-toggle="modal" data-target="#addTeam-modal"><i class="fa fa-plus-circle"></i> Add</a>\n        </div>\n      </div>\n')
        # SOURCE LINE 109
        for id, team in enumerate(c.teams):
            # SOURCE LINE 110
            __M_writer(u'        <div class="well team team-')
            __M_writer(escape(team["id"]))
            __M_writer(u'">\n          <img class="team-avatar" src="/images/teams/')
            # SOURCE LINE 111
            __M_writer(escape(team["id"]))
            __M_writer(u'.jpg">\n          <div class="details">\n            <h3><i class="fa fa-users"></i> ')
            # SOURCE LINE 113
            __M_writer(escape(team["name"]))
            __M_writer(u'</h3>\n            <h3><i class="fa fa-globe"></i> ')
            # SOURCE LINE 114
            __M_writer(escape(team["country"]))
            __M_writer(u'</h3>\n            <h3><i class="fa fa-trophy"></i> ')
            # SOURCE LINE 115
            __M_writer(escape(c.league["name"]))
            __M_writer(u' &bull; ')
            __M_writer(escape(c.league["region"]))
            __M_writer(u' &bull; ')
            __M_writer(escape(c.league["type"]))
            __M_writer(u'</h3>\n          </div>\n          <div class="pull-right">\n            <div class="btn-group btn-block">\n              <button class="btn btn-md btn-primary editTeam-button" data-json=\'')
            # SOURCE LINE 119
            __M_writer(escape(team["json"]))
            __M_writer(u'\'><i class="fa fa-pencil"></i> Edit</button>\n              <button class="btn btn-md btn-primary removeTeam-button" data-id="')
            # SOURCE LINE 120
            __M_writer(escape(team["id"]))
            __M_writer(u'"><i class="fa fa-times-circle"></i> Remove</button>\n            </div>\n          </div>\n        </div>\n')
        # SOURCE LINE 125
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


