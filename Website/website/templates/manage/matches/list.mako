<%namespace name="partials" file="../partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="modal fade" id="removeMatch-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-times-circle"></i> Remove</h3>
      </div>
      <div class="modal-body">
        <p>Are you sure you want to delete this match?</p>
        <div class="btn-group">
          <button id="removeMatch-confirm" class="btn btn-primary">Yes</button>
          <button data-dismiss="modal" aria-hidden="true" class="btn btn-primary float-right">No</button>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="addMatch-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-plus-circle"></i> Add</h3>
      </div>
      <div class="modal-body">
        <form role="form" id="addMatch-form" method="POST" action="/manage/matches/${c.league["id"]}/add/" enctype="multipart/form-data">
          <div class="form-group">
            <label for="team1">Team 1</label>
            <select name="team1" class="form-control">
              %for team in c.teams:
                <option value="${team["id"]}">${team["name"]}</option>
              %endfor
            </select>
          </div>
          <div class="form-group">
            <label for="team2">Team 2</label>
            <select name="team2" class="form-control">
              %for team in c.teams:
                <option value="${team["id"]}">${team["name"]}</option>
              %endfor
            </select>
          </div>
          <div class="form-group">
            <label for="stream">Stream</label>
            <input name="stream" class="form-control" type="text">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="editMatch-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-pencil"></i> Edit</h3>
      </div>
      <div class="modal-body">
        <form role="form" id="editMatch-form">
          <div class="form-group">
            <label for="team1">Team 1</label>
            <select name="team1" class="form-control">
              %for team in c.teams:
                <option value="${team["id"]}">${team["name"]}</option>
              %endfor
            </select>
          </div>
          <div class="form-group">
            <label for="team2">Team 2</label>
            <select name="team2" class="form-control">
              %for team in c.teams:
                <option value="${team["id"]}">${team["name"]}</option>
              %endfor
            </select>
          </div>
          <div class="form-group">
            <label for="stream">Stream</label>
            <input name="stream" class="form-control" type="text">
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
        <h2><i class="fa fa-users"></i> Matches</h2>
        <div class="button-panel pull-right">
          <a href="/manage/matches/" class="btn btn-md btn-primary"><i class="fa fa-reply"></i> Back</a>
          <a class="btn btn-md btn-primary" data-toggle="modal" data-target="#addMatch-modal"><i class="fa fa-plus-circle"></i> Add</a>
        </div>
      </div>
      %for id, match in enumerate(c.matches):
        <div class="well match match-${match["id"]}">
          <div class="row">
            <div class="col-md-9">
              <div class="row">
                <div class="col-md-6">
                  <div class="team-0-avatar">
                    <img class="team-avatar" src="/images/teams/${match["team1"]["id"]}.jpg">
                  </div>
                  <h3 class="team-0">${match["team1"]["name"]}</h3>
                </div>
                <div class="col-md-6">
                  <div class="team-1-avatar">
                    <img class="team-avatar" src="/images/teams/${match["team2"]["id"]}.jpg">
                  </div>
                  <h3 class="team-1">${match["team2"]["name"]}</h3>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="btn-group btn-block">
                <button class="btn btn-md btn-primary editMatch-button" data-json="${match["json"]}"><i class="fa fa-pencil"></i> Edit</button>
                <button class="btn btn-md btn-primary removeMatch-button" data-id="${match["id"]}"><i class="fa fa-times-circle"></i> Remove</button>
              </div>
            </div>
          </div>
        </div>
      %endfor
    </div>
  </div>
</div>