<%inherit file="/base.mako" />

<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="modal fade" id="inventory-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-gavel"></i> Bet</h3>
      </div>
      <div class="modal-body">
        <p class="connection-status"><i class="fa fa-spinner fa-spin"></i> Establishing connection with bot</p>
      </div>
    </div>
  </div>
</div>
<div class="container bets">
  <div class="clearfix well bet ${c.match["league"]["name"]} text-center" data-id="${c.match["id"]}">
    <div class="league-badge" style="background-color: #${c.match["league"]["colour"]};">
      <img src="/images/leagues/${c.match["league"]["id"]}/logo.png">
    </div>
    %for id, team in enumerate(c.match["teams"]):
      <div class="team-${id}">
        %if id is 0:
          <img src="/images/teams/${team["id"]}.jpg">
        %endif
        <div class="details">
          <h2>${team["name"]}</h2>
          <span class="specifics">
            <p>
              %if c.match["bet"] is False:
                <button class="btn btn-md btn-primary btn-inventory" data-match="${c.match["id"]}" data-team="${team["id"]}" data-toggle="modal" data-target="#inventory-modal"><i class="fa fa-gavel"></i> Bet</button>
              %elif c.match["bet"] == team["id"]:
                <button class="btn btn-md btn-primary btn-inventory" data-match="${c.match["id"]}" data-team="${team["id"]}" data-toggle="modal" data-target="#inventory-modal"><i class="fa fa-usd"></i> Raise</button>
              %else:
                <a class="btn btn-md btn-primary" href="/bet/${c.match["id"]}/switch/"><i class="fa fa-refresh"></i> Switch</a>
              %endif
            </p>
            <p><i class="fa fa-thumbs-up"></i> ${team["bets"]["percentage"]}%</p>
          </span>
        </div>
        %if id is 1:
            <img src="/images/teams/${team["id"]}.jpg">
        %endif
      </div>
    %endfor
</div>