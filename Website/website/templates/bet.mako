<%namespace name="partials" file="partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <title>${c.match["teams"][c.match["teamsOrder"][0]]["name"]} against ${c.match["teams"][c.match["teamsOrder"][1]]["name"]} &bull; Saloon.tf</title>
  <script type="text/javascript">
    var betID = ${c.match["id"]};
  </script>
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
  ${partials.bet(c.match)}
  <div class="row bets-row">
    <div class="col-md-6 left">
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
    </div>
    <div class="col-md-6 right">
    </div>
  </div>
</div>