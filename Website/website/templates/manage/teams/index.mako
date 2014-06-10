<%inherit file="/base.mako" />

<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="container manage">
  <div class="row">
    <%namespace name="partials" file="../partials.mako"/>
    ${partials.menu()}
    <div class="col-sm-9">
      <div class="header">
        <h2><i class="fa fa-users"></i> Teams</h2>
        <h3><i class="fa fa-filter"></i> Filters</h3>
      </div>
      <div class="well">
        %for league in c.leagues:
          <a href="/manage/teams/${league["id"]}/">
            <span class="league-block ${league["name"]}">
              <div class="league-badge" style="background-color: #${league["colour"]};">
                <img src="/images/leagues/${league["id"]}/logo.png">
              </div>
              <div class="details-overlay">
                <h3><i class="fa fa-globe"></i> ${league["region"]}</h3>
                <h3><i class="fa fa-flag"></i> ${league["type"]}</h3>
              </div>
            </span>
          </a>
        %endfor
      </div>
    </div>
  </div>
</div>