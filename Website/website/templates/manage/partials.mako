<%block name="menu">
  <div class="col-sm-3">
    <div class="list-group">
      <a href="/manage/" class="list-group-item ${'active' if c.managePage == "dashboard" else ''}">
        <i class="fa fa-th-large"></i> Dashboard
      </a>
      %if c.user["permissions"].leagues:
        <a href="/manage/leagues/" class="list-group-item ${'active' if c.managePage == "leagues" else ''}"><i class="fa fa-trophy"></i> Leagues</a>
      %endif
      %if c.user["permissions"].teams:
        <a href="/manage/teams/" class="list-group-item ${'active' if c.managePage == "teams" else ''}"><i class="fa fa-users"></i> Teams</a>
      %endif
      %if c.user["permissions"].bets:
        <a href="/manage/matches/" class="list-group-item ${'active' if c.managePage == "matches" else ''}"><i class="fa fa-gavel"></i> Matches</a>
      %endif
      %if c.user["permissions"].users:
        <a href="#" class="list-group-item"><i class="fa fa-user"></i> Users</a>
      %endif
      %if c.user["permissions"].bets:
        <a href="#" class="list-group-item"><i class="fa fa-ticket"></i> Tickets</a>
      %endif
    </div>
  </div>
</%block>
<%block name="dashboardBets">
  <div class="col-sm-12">
    <div class="panel panel-primary">
      <div class="panel-heading"><i class="fa fa-bar-chart-o"></i> Bets</div>
      <div class="panel-body">
        <p>Placeholder for bets chart.</p>
      </div>
    </div>
  </div>
</%block>
<%block name="dashboardFixtures">
  <div class="col-sm-6">
    <div class="panel panel-primary">
      <div class="panel-heading"><i class="fa fa-list"></i> Fixtures</div>
      <div class="panel-body">
        <p>Placeholder for upcoming fixtures list.</p>
      </div>
    </div>
  </div>
</%block>