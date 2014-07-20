<%def name="bet(match)">
  <div class="clearfix well bet ${match["league"]["name"]} text-center" data-id="${match["id"]}">
    <div class="league-badge" style="background-color: #${match["league"]["colour"]};">
      <img src="/images/leagues/${match["league"]["id"]}/logo.png">
    </div>
    %for index, id in enumerate(match["teamsOrder"]):
      <% team = match["teams"][id] %>
      <div class="team-${index}">
        %if index is 0:
          <img src="/images/teams/${team["id"]}.jpg">
        %endif
        <div class="details">
          <h2>${team["name"]}</h2>
          <span class="specifics">
            <p>
              %if match["status"] == 0:
                %if match["bet"] is False:
                  %if c.user:
                    <button class="btn btn-md btn-primary btn-inventory" data-match="${match["id"]}" data-team="${team["id"]}" data-toggle="modal" data-target="#inventory-modal"><i class="fa fa-gavel"></i> Bet</button>
                  %else:
                    <a class="btn btn-md btn-primary" href="/login/"><i class="fa fa-gavel"></i> Bet</a>
                  %endif
                %else:
                  %if match["bet"] == team["id"]:
                    <button class="btn btn-md btn-primary btn-inventory" data-match="${match["id"]}" data-team="${team["id"]}" data-toggle="modal" data-target="#inventory-modal"><i class="fa fa-usd"></i> Raise</button>
                  %else:
                    <a class="btn btn-md btn-primary" href="/bet/${match["id"]}/switch/"><i class="fa fa-refresh"></i> Switch</a>
                  %endif
                %endif
              %elif match["status"] == 1 or match["status"] == 2:
                <i class="fa fa-flag"></i> ${team["points"]} ${"point" if team["points"] == 1 else "points"}
              %endif
            </p>
            <p><i class="fa fa-thumbs-up"></i> ${team["bets"]["percentage"]}%</p>
          </span>
        </div>
        %if index is 1:
            <img src="/images/teams/${team["id"]}.jpg">
        %endif
      </div>
    %endfor
  </div>
</%def>