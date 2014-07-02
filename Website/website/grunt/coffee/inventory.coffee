openConnection = (type) ->
  $("#" + type + "-modal .modal-body").html "
    <p class=\"connection-status\">
      <i class=\"fa fa-spinner fa-spin\"></i> Establishing connection with bot
    </p>
  "
  socket = new WebSocket("ws://ssh.saloon.tf:9000")
  socket.onopen = ->
    $(".connection-status").html "<i class=\"fa fa-check\"></i> Connected"
    $("#" + type + "-modal .modal-body").append "
      <p class=\"authentication-status\">
        <i class=\"fa fa-spinner fa-spin\"></i> Authenticating
      </p>
    "
    json = JSON.stringify([
      "hello"
      type
      steamID
    ])
    socket.send json
    return

  socket.onclose = ->
    $("#" + type + "-modal").modal "hide"
    return

  socket.onmessage = (event) ->
    array = JSON.parse(event.data)
    console.log array

    if array[0] is "hello"
      botArray = array.slice(0)
      $(".authentication-status").html "<i class=\"fa fa-check\"></i> Authenticated"
      if type is "deposit"
        $("#deposit-modal .modal-body").append "
          <p>
            <i class=\"fa fa-question\"></i> Select items that you want to deposit from your inventory and press accept.
          </p>
        "
      else if type is "withdraw"
        $(".queue-status").remove()  if $(".queue-status").length > 0
        $("#withdraw-modal .modal-body").append "
          <p>
            <i class=\"fa fa-question\"></i> Select items that you want to withdraw from bots inventory and press accept.
          </p>
        "
      $("#" + type + "-modal .modal-body").append "
        <p class=\"button-paragraph\">
          <button id=\"trade-button\" class=\"btn btn-md btn-primary btn-block\">
            <i class=\"fa fa-exchange\"></i> Trade
          </button>
        </p>
      "
      $("#" + type + "-modal .modal-body #trade-button").on "click", ->
        window.open "http://saloon.tf/trade/" + botArray[1] + "/", "_blank"
        $("#" + type + "-modal .modal-body .button-paragraph").remove()
        if type is "deposit"
          $("#deposit-modal .modal-body").append "
            <p class=\"trade-status\">
              <i class=\"fa fa-spinner fa-spin\"></i> Waiting for trade to be processed
            </p>
          "
        return

      if type is "withdraw"
        $("#withdraw-modal .modal-body").append "
          <div class=\"progress\">
            <div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"100\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 100%\">
            </div>
          </div>
        "
        $("#withdraw-modal .modal-body .progress-bar").addClass "countdown"
        setTimeout (->
          $("#withdraw-modal .modal-body .progress-bar").css "width", "0%"
          return
        ), 1000
    else if array[0] is "queue"
      queueArray = array.slice(0)
      if queueArray[1] is "position"
        suffix = (queueArray[2] | 0) % 100
        suffix = (if suffix > 3 and suffix < 21 then "th" else [
          "th"
          "st"
          "nd"
          "rd"
        ][suffix % 10] or "th")
        if $(".queue-status").length > 0
          $(".queue-status").html "<i class=\"fa fa-users\"></i> You&rsquo;re " + queueArray[2] + suffix + " in the queue."
        else
          $(".authentication-status").html "<i class=\"fa fa-check\"></i> Authenticated"
          $("#withdraw-modal .modal-body").append "
            <p class=\"queue-status\">
              <i class=\"fa fa-spinner fa-spin\"></i> You&rsquo;re " + queueArray[2] + suffix + " in the queue.
            </p>
          "
    else if array[0] is "accepted"
      $(".trade-status").html "<i class=\"fa fa-check\"></i> Trade completed!"
      window.setTimeout (->
        window.open "http://saloon.tf/inventory/", "_self"
        return
      ), 3000
    else if array[0] is "declined"
      $(".trade-status").html "<i class=\"fa fa-times\"></i> There was an error in the trade."
      window.setTimeout (->
        window.open "http://saloon.tf/inventory/", "_self"
        return
      ), 3000
    return
  return

socket = undefined
$ ->
  if page is "inventory"
    $("#deposit-modal").on "shown.bs.modal", (e) ->
      openConnection "deposit"
      return

    $("#deposit-modal").on "hidden.bs.modal", (e) ->
      socket.close()
      return

    $("#withdraw-modal").on "shown.bs.modal", (e) ->
      openConnection "withdraw"
      return

    $("#withdraw-modal").on "hidden.bs.modal", (e) ->
      socket.close()
      return
  return