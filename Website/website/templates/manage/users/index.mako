<%namespace name="partials" file="../partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="container manage">
  <div class="row">
    ${partials.menu()}
    <div class="col-sm-9">
      <div class="header">
        <h2><i class="fa fa-users"></i> Users</h2>
        <h3><i class="fa fa-search"></i> Search</h3>
      </div>
      <div class="well search">
        <div class="input-group">
          <span class="input-group-addon"><i class="fa fa-search"></i></span>
          <input id="user-search" type="text" class="form-control" placeholder="Username">
        </div>
      </div>
    </div>
  </div>
</div>