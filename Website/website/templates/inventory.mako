<%inherit file="/base.mako" />

<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
<div class="modal fade" id="deposit-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-sign-in"></i> Deposit</h3>
      </div>
      <div class="modal-body">
        <p class="connection-status"><i class="fa fa-spinner fa-spin"></i> Establishing connection with bot</p>
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="withdraw-modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 class="modal-title"><i class="fa fa-sign-out"></i> Withdraw</h3>
      </div>
      <div class="modal-body">
        <p class="connection-status"><i class="fa fa-spinner fa-spin"></i> Establishing connection with bot</p>
      </div>
    </div>
  </div>
</div>
<div class="container">
  <div class="header">
    <h2><i class="fa fa-briefcase"></i> Inventory</h2>
    <div class="button-panel pull-right">
      <button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#deposit-modal"><i class="fa fa-sign-in"></i> Deposit</button>
        %if c.hasItems:
          <button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#withdraw-modal"><i class="fa fa-sign-out"></i> Withdraw</button>
        %endif
    </div>
  </div>
  <div class="items well">
    %if c.hasItems:
      %for index, name in enumerate(c.items["names"]):
        %for item in range(0, c.items["quantity"][index]):
          <div class="item ${name}">
            <div class="check"><i class="fa fa-check"></i></div>
            <img src="/images/items/${name}.png">
          </div>
        %endfor
      %endfor
    %else:
      <p class="text-center">You don't have any items yet.<br>Please deposit some before you start betting.</p>
      <p class="text-center"><button class="btn btn-lg btn-primary" data-toggle="modal" data-target="#deposit-modal"><i class="fa fa-sign-in"></i> Deposit</button></p>
    %endif
  </div>
</div>