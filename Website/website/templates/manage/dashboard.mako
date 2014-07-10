<%namespace name="partials" file="partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="container manage">
  <div class="row">
    ${partials.menu()}
    <div class="col-sm-9">
      <div class="header">
        <h2><i class="fa fa-th-large"></i> Dashboard</h2>
        <div class="button-panel pull-right">
          <button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#addLeague-modal"><i class="fa fa-refresh"></i> Refresh</button>
        </div>
      </div>
      <div class="row">
        ${partials.dashboardBets()}
        ${partials.dashboardFixtures()}
        ${partials.dashboardFixtures()}
      </div>
    </div>
  </div>
</div>