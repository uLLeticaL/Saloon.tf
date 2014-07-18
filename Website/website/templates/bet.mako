<%namespace name="partials" file="partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <!-- add some head tags here -->
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
<div class="container bets">
  ${partials.bet(c.match)}
  <div class="row bets-row">
    <div class="col-md-6 left">
      %if c.match["ownbet"]:        
        <div class="bet-details panel panel-default animated fadeInUp">
          <div class="panel-heading">
            You've placed a bet on <strong>${c.match["ownbet"]["team"]["name"]}</strong>
          </div>
          <div class="panel-body">
            <div class="inventory-wrapper">
              <div class="inventory">
                %for group in c.match["ownbet"]["groups"]:
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