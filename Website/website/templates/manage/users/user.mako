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
        <h2><i class="fa fa-user"></i> Edit User: ${c.RTargetUser["name"]}</h2>
      </div>
      <div class="well">
        <form role="form" id="editUser-form" method="post">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" name="name" value="${c.RTargetUser["name"]}">
          </div>
          <div class="form-group">
            <label for="name">Avatar</label>
            <input type="text" class="form-control" name="avatar" value="${c.RTargetUser["avatar"]}">
          </div>
          <div class="form-group">
            <label for="name">SteamID</label>
            <input type="text" class="form-control" name="steamid" value="${c.RTargetUser["steamID"]}">
          </div>
          <p>
            <label>Bot</label><br>
            <select name="bot" class="form-control">
              %for bot in c.bots:
                <option value="${bot["id"]}">${bot["id"]} - ${bot["name"]}</option>
              %endfor
            </select>
          </p>
          <button type="submit" class="btn btn-lg btn-primary">Submit</button>
        </form>
    </div>
  </div>
</div>
