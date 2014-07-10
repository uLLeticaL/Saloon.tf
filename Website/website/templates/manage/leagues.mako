<%namespace name="partials" file="partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="modal fade" id="removeLeague-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-times-circle"></i> Remove</h3>
      </div>
      <div class="modal-body">
        <p>Are you sure you want to delete this league?</p>
        <div class="btn-group">
          <button id="removeLeague-confirm" class="btn btn-primary">Yes</button>
          <button data-dismiss="modal" aria-hidden="true" class="btn btn-primary float-right">No</button>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="addLeague-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-plus-circle"></i> Add</h3>
      </div>
      <div class="modal-body">
        <form role="form" id="addLeague-form" method="POST" action="/manage/leagues/add/" enctype="multipart/form-data">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" name="name" placeholder="Enter name">
          </div>
          <p>Type<br>
          <div class="btn-group" data-toggle="buttons">
            <label class="btn btn-primary">
              <input type="radio" name="type" value="6on6"> 6on6
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="type" value="Highlander"> Highlander
            </label>
          </div>
          </p>
          <p>Region<br>
          <div class="btn-group" data-toggle="buttons">
            <label class="btn btn-primary">
              <input type="radio" name="region" value="North America"> North America
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="South America"> South America
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="Europe"> Europe
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="Asia"> Asia
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="Australia and Oceania"> Australia and Oceania
            </label>
          </div>
          </p>
          <p>Avatar</p>
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
            <label for="accentColour">Colour</label>
            <input type="text" class="form-control" name="accentColour" id="accentColour" placeholder="222222">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="editLeague-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-pencil"></i> Edit</h3>
      </div>
      <div class="modal-body">
        <form role="form" id="editLeague-form">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" name="name" placeholder="Enter name">
          </div>
          <p>Type<br>
          <div class="btn-group" data-toggle="buttons">
            <label class="btn btn-primary">
              <input type="radio" name="type" value="6on6"> 6on6
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="type" value="Highlander"> Highlander
            </label>
          </div>
          </p>
          <p>Region<br>
          <div class="btn-group" data-toggle="buttons">
            <label class="btn btn-primary">
              <input type="radio" name="region" value="North America"> North America
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="South America"> South America
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="Europe"> Europe
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="Asia"> Asia
            </label>
            <label class="btn btn-primary">
              <input type="radio" name="region" value="Australia and Oceania"> Australia and Oceania
            </label>
          </div>
          </p>
          <div class="form-group">
            <label for="accentColour">Colour</label>
            <input type="text" class="form-control" name="accentColour" id="accentColour" placeholder="222222">
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
        <h2><i class="fa fa-trophy"></i> Leagues</h2>
        <div class="button-panel pull-right">
          <button class="btn btn-md btn-primary" data-toggle="modal" data-target="#addLeague-modal"><i class="fa fa-plus-circle"></i> Add</button>
        </div>
      </div>
      %for league in c.leagues:
        <div class="well league ${league["name"]}">
          <div class="league-badge" style="background-color: #${league["colour"]};">
            <img src="/images/leagues/${league["id"]}/logo.png">
          </div>
          <div class="details">
            <h3><i class="fa fa-trophy"></i> ${league["name"]}</h3>
            <h3><i class="fa fa-globe"></i> ${league["region"]}</h3>
            <h3><i class="fa fa-flag"></i> ${league["type"]}</h3>
          </div>
          <div class="pull-right">
            <div class="btn-group btn-block">
              <button class="btn btn-md btn-primary editLeague-button" data-json='${league["json"]}'><i class="fa fa-pencil"></i> Edit</button>
              <button class="btn btn-md btn-primary removeLeague-button" data-id="${league["id"]}"><i class="fa fa-times-circle"></i> Remove</button>
            </div>
          </div>
        </div>
      %endfor
    </div>
  </div>
</div>