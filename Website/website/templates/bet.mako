<%namespace name="partials" file="partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <title>${c.match["teams"][c.match["teamsOrder"][0]]["name"]} against ${c.match["teams"][c.match["teamsOrder"][1]]["name"]} &bull; Saloon.tf</title>
  <script type="text/javascript">
    var betID = ${c.match["id"]};
    var teams = ${c.match["teamsJson"] | n}
  </script>
</%def>
<%def name="bet()">
  %if c.match["bet"]:
    <div class="bet-details panel panel-default animated fadeInUp">
      <div class="panel-heading ${"heading-won" if c.match["betStatus"] == 1 else ""}">
        %if c.match["betStatus"] == 1 or c.match["status"] == 2:
          <span>You've placed a bet on <strong>${c.match["teams"][c.match["bet"]]["name"]}</strong> and won!</span>
          %if c.match["betStatus"] == 1:
            <button class="btn btn-md btn-primary btn-payout pull-right"><i class="fa fa-briefcase"></i> Payout</button>
          %else:
            <a href="http://steamcommunity.com/tradeoffer/${c.match["betOffer"]}/" class="btn btn-md btn-primary btn-payout pull-right"><i class="fa fa-refresh"></i> Trade</a>
          %endif
        %else:
          <span>You've placed a bet on <strong>${c.match["teams"][c.match["bet"]]["name"]}</strong></span>
        %endif
      </div>
      <div class="panel-body">
        <div class="inventory-wrapper">
          <div class="inventory">
            %if c.match["betStatus"] == 1 or c.match["betStatus"] == 2:
              %for group in c.match["wonGroups"]:
                %for item in range(group[2]):
                  <div class="steam-item quality-${group[1]}" style="background-image:url('/images/items/${group[0]}.png')">
                    <div class="value">New</div>
                  </div>
                %endfor
              %endfor
            %endif
            %for group in c.match["betGroups"]:
              %for item in range(group[2]):
                <div class="steam-item quality-${group[1]}" style="background-image:url('/images/items/${group[0]}.png')"></div>
              %endfor
            %endfor
          </div>
        </div>
      </div>
    </div>
  %endif
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
<div class="modal fade" id="payout-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-sign-out"></i> Payout</h3>
      </div>
      <div class="modal-body">
        <p class="connection-status"><i class="fa fa-spinner fa-spin"></i> Establishing connection with bot</p>
      </div>
    </div>
  </div>
</div>
<div class="container bets">
  ${partials.match(c.match)}
  %if c.match["stream"] and c.match["status"] == 1:
    <div class="stream-row has-panel">
      <div class="stream">
        <span class="loading"><i class="fa fa-circle-o-notch fa-spin"></i> Loading player</span>
        <object wmode="transparent" type="application/x-shockwave-flash" id="live_embed_player_flash" data="http://www.twitch.tv/widgets/live_embed_player.swf?channel=${c.match["stream"]}" bgcolor="#000000">
          <param name="allowFullScreen" value="true">
          <param name="allowScriptAccess" value="always">
          <param name="allowNetworking" value="all">
          <param name="movie" value="http://www.twitch.tv/widgets/live_embed_player.swf">
          <param name="flashvars" value="hostname=www.twitch.tv&amp;channel=${c.match["stream"]}&amp;auto_play=true&amp;start_volume=25">
        </object>
      </div>
      <ul class="logs">
        <li class="list-group-item logs-header">
          <h3>
            <img class="avatar-sm" src="/images/teams/${c.match["teams"][c.match["teamsOrder"][0]]["id"]}.jpg">
            <span class="logs-score-0">0</span> - <span class="logs-score-1">0</span>
            <img class="avatar-sm" src="/images/teams/${c.match["teams"][c.match["teamsOrder"][1]]["id"]}.jpg">
          </h3>
        </li>
        <li class="list-group-item logs-item">&nbsp;</li>
        <li class="list-group-item logs-item">&nbsp;</li>
        <li class="list-group-item logs-item">&nbsp;</li>
        <li class="list-group-item logs-item">&nbsp;</li>
        <li class="list-group-item logs-item">&nbsp;</li>
        <li class="list-group-item logs-item">&nbsp;</li>
        <li class="list-group-item logs-item">&nbsp;</li>
      </ul>
    </div>
  %endif
  <div class="row bets-row">
    <div class="col-md-6 left">
      ${self.bet()}
    </div>
    <div class="col-md-6 right">
    </div>
  </div>
</div>