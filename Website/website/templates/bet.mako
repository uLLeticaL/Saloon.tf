<%inherit file="/base.mako" />

<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
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