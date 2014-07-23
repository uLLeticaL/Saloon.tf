<%namespace name="partials" file="../partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="modal fade" id="removeTeam-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-times-circle"></i> Remove</h3>
      </div>
      <div class="modal-body">
        <p>Are you sure you want to delete this team?</p>
        <div class="btn-group">
          <button id="removeTeam-confirm" class="btn btn-primary">Yes</button>
          <button data-dismiss="modal" aria-hidden="true" class="btn btn-primary float-right">No</button>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="addTeam-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-plus-circle"></i> Add</h3>
      </div>
      <div class="modal-body">
        <form role="form" id="addTeam-form" method="POST" action="/manage/teams/${c.league["id"]}/add/" enctype="multipart/form-data">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" name="name" placeholder="Enter name">
          </div>
          <p>
            Country<br>
            <select name="country" class="form-control">
              %for country in c.countries:
                <option value="${country["id"]}">${country["name"]}</option>
              %endfor
            </select>
          </p>
          Avatar<br>
          <div class="fileinput fileinput-new input-group" data-provides="fileinput">
            <div class="form-control fileinput-control" data-trigger="fileinput">
              <i class="fa fa-file"></i> <span class="fileinput-filename"></span>
            </div>
            <span class="input-group-addon btn btn-default btn-file">
              <span class="fileinput-new">Select file</span>
              <span class="fileinput-exists">Change</span>
              <input type="file" name="avatar">
            </span>
            <a href="#" class="input-group-addon btn btn-default fileinput-exists" data-dismiss="fileinput">Remove</a>
          </div>
          <div class="form-group">
            <label for="name">LeagueID</label>
            <input type="text" class="form-control" name="leagueID" placeholder="Enter LeagueID">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="editTeam-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-pencil"></i> Edit</h3>
      </div>
      <div class="modal-body">
        <form role="form" id="editTeam-form">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" name="name" placeholder="Enter name">
          </div>
          <p>
            Country<br>
            <select name="country" class="form-control">
              %for country in c.countries:
                <option value="${country["id"]}">${country["name"]}</option>
              %endfor
            </select>
          </p>
          <div class="form-group">
            <label for="name">LeagueID</label>
            <input type="text" class="form-control" name="leagueID" placeholder="Enter LeagueID">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</div>
<div class="container manage">
  <div class="row">
    ${partials.menu()}
    <div class="col-sm-9">
      <div class="header">
        <h2><i class="fa fa-users"></i> Teams</h2>
        <div class="button-panel pull-right">
          <a href="/manage/teams/" class="btn btn-md btn-primary"><i class="fa fa-reply"></i> Back</a>
          <a class="btn btn-md btn-primary" data-toggle="modal" data-target="#addTeam-modal"><i class="fa fa-plus-circle"></i> Add</a>
        </div>
      </div>
      %if c.teams:
        %for id, team in enumerate(c.teams):
          <div class="well team team-${team["id"]}">
            <img class="team-avatar" src="/images/teams/${team["id"]}.jpg">
            <div class="details">
              <h3><i class="fa fa-users"></i> ${team["name"]}</h3>
              <h3><i class="fa fa-globe"></i> ${team["country"]}</h3>
              <h3><i class="fa fa-trophy"></i> ${c.league["name"]} &bull; ${c.league["region"]} &bull; ${c.league["type"]}</h3>
            </div>
            <div class="pull-right">
              <div class="btn-group btn-block">
                <button class="btn btn-md btn-primary editTeam-button" data-json='${team["json"]}'><i class="fa fa-pencil"></i> Edit</button>
                <button class="btn btn-md btn-primary removeTeam-button" data-id="${team["id"]}"><i class="fa fa-times-circle"></i> Remove</button>
              </div>
            </div>
          </div>
        %endfor
      %else:
        <div class="well text-center">
          Please use the top toolbar to add a new fixture.
        </div>
      %endif
    </div>
  </div>
</div>