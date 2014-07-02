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
        <h2><i class="fa fa-user"></i> ${c.otherUser["name"]}</h2>
      </div>
      <div class="well">
        <form role="form" id="editUser-form" method="post">
          <div class="form-group">
            <label for="name">Steam</label>
            <input type="text" class="form-control" name="steamid" value="${c.otherUser["steamid"]}">
          </div>
          <div class="form-group">
            <label for="botID">Bot</label>
            <select name="botID" class="form-control">
              %for bot in c.bots:
                <option ${'selected' if bot["id"] == c.otherUser["botID"] else ''} value="${bot["id"]}">#${bot["id"]} ${bot["name"]}</option>
              %endfor
            </select>
          </div>
          %if c.user["permissions"].permissions:
            <p>Permissions</p>
            <p>
              <div class="btn-group" data-toggle="buttons">
                <label class="btn btn-primary ${'active' if c.otherUser["permissions"].manage else ''}">
                  <input type="checkbox" name="permissions" value="manage" ${'checked' if c.otherUser["permissions"].manage else ''}> Manage
                </label>
                <label class="btn btn-primary ${'active' if c.otherUser["permissions"].leagues else ''}">
                  <input type="checkbox" name="permissions" value="leagues" ${'checked' if c.otherUser["permissions"].leagues else ''}> Leagues
                </label>
                <label class="btn btn-primary ${'active' if c.otherUser["permissions"].teams else ''}">
                  <input type="checkbox" name="permissions" value="teams" ${'checked' if c.otherUser["permissions"].teams else ''}> Teams
                </label>
                <label class="btn btn-primary ${'active' if c.otherUser["permissions"].bets else ''}">
                  <input type="checkbox" name="permissions" value="bets" ${'checked' if c.otherUser["permissions"].bets else ''}> Bets
                </label>
                <label class="btn btn-primary ${'active' if c.otherUser["permissions"].users else ''}">
                  <input type="checkbox" name="permissions" value="users" ${'checked' if c.otherUser["permissions"].users else ''}> Users
                </label>
                <label class="btn btn-primary ${'active' if c.otherUser["permissions"].bots else ''}">
                  <input type="checkbox" name="permissions" value="bots" ${'checked' if c.otherUser["permissions"].bots else ''}> Bots
                </label>
              </div>
            </p>
          %endif
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
  </div>
</div>
