<%inherit file="/base.mako" />

<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="container bets">
  <div class="header">
    <h2><i class="fa fa-gavel"></i> Bets</h2>
  </div>
  %for match in c.matches:
    <div class="well bet ${match["league"]["name"]} text-center" data-id="${match["id"]}">
      <div class="league-badge" style="background-color: #${match["league"]["colour"]};">
        <img src="/images/leagues/${match["league"]["id"]}/logo.png">
      </div>
      %for id, team in enumerate(match["teams"]):
        <div class="team-${id}">
          %if id is 0:
            <img src="/images/teams/${team["id"]}.jpg">
          %endif
          <div class="details">
            <h3>${team["name"]}</h3>
            <span class="specifics">
              <p><button class="btn btn-block btn-md btn-primary"><i class="fa fa-gavel"></i> Bet</button></p>
              <p><i class="fa fa-thumbs-up"></i> ${team["bets"]["percentage"]}%</p>
            </span>
          </div>
          %if id is 1:
            <img src="/images/teams/${team["id"]}.jpg">
          %endif
        </div>
      %endfor
    </div>
  %endfor
</div>