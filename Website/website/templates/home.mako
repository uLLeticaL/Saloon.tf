<%namespace name="partials" file="partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <title>Saloon.tf &bull; Home</title>
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
  %for match in c.matches:
    ${partials.match(match)}
  %endfor
</div>