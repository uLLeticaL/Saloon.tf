$ ->
  if page is "bet"
    offset = 0
    loadBets = ->
      $.getJSON "/api/bet/" + betID + "/bets/offset/" + offset, (data) ->
        console.log data
        for number, bet of data
          $element = $ "
            <div class=\"bet-details panel panel-default animated fadeInUp\">
              <div class=\"panel-heading\">
                " + bet["user"]["name"] + " placed a bet on <strong>" + bet["team"]["name"] + "</strong>
              </div>
              <div class=\"panel-body\">
                <div class=\"inventory-wrapper\">
                  <div class=\"inventory\">
                  </div>
                </div>
              </div>
            </div>
          "
          for index, item of bet["items"]
            for i in [0...item["amount"]]
              $element.find(".inventory").append "<div class=\"steam-item " + item["name"] + "\"></div>"
          if $(".bets-row .col-md-6.right").height() > $(".bets-row .col-md-6.left").height()
            $(".bets-row .col-md-6.left").append $element
          else
            $(".bets-row .col-md-6.right").append $element
        return
      return
    loadBets()

  if page is "bet" or page is "home"
    team = undefined
    match = undefined
    bot = undefined
    socket = new WebSocket("ws://direct."  + window.location.host + ":9000")

    socket.onopen = ->
      return

    socket.onclose = ->
      $("#inventory-modal").modal "hide"
      return

    socket.onmessage = (event) ->
      array = JSON.parse(event.data)
      console.log array
      $(".connection-status").html "<i class=\"fa fa-check\"></i> Connected"
      if array[0] is "hello"
        bot = array[1]
        $(".connection-status").html "<i class=\"fa fa-check\"></i> Connected"
        $("#inventory-modal .modal-body").append "
          <p class=\"authentication-status\">
            <i class=\"fa fa-exclamation-circle\"></i> Bot sent you an invintation</a>
          </p>
        "
      else if array[0] is "tradeLink"
        if array[1] is "new"
          $("#inventory-modal .modal-body").append "
            <div class=\"form-group tradelink-form\">
              <label for=\"tradelink-input\"><i class=\"fa fa-exclamation-circle\"></i> Please paste your tradeoffers link below</label>
                <input class=\"form-control tradelink-input\" name=\"tradelink-input\">
            </div>
          "
          $(".tradelink-input").on "keyup", (e) ->
            $(this).parent().removeClass("has-error")
            if e.which is 13
              json = JSON.stringify([
                "tradeLink"
                $(".tradelink-input").val()
              ])
              socket.send json
            return
        else if array[1] is "wrong"
          $(".tradelink-form").addClass("has-error")
      else if array[0] is "inventory"
        inventory = array[1]
        $("#inventory-modal .modal-body").html "
          <div class=\"carousel-inventory-wrapper\">
            <div id=\"carousel-inventory\" class=\"carousel slide\">
              <div class=\"carousel-inner\">
                <div class=\"item active\"><div class=\"inventory-wrapper\"><div class=\"inventory\"></div></div></div>
              </div>
            </div>
            <a class=\"left carousel-inventory-control carousel-control\" href=\"#carousel-inventory\" role=\"button\" data-slide=\"prev\">
              <span class=\"fa fa-chevron-left\"></span>
            </a>
            <a class=\"right carousel-inventory-control carousel-control\" href=\"#carousel-inventory\" role=\"button\" data-slide=\"next\">
              <span class=\"fa fa-chevron-right\"></span>
            </a>
          </div>
          <div class=\"btn-bet-wrapper\">
            <button class=\"btn btn-primary btn-bet disabled\"><i class=\"fa fa-gavel\"></i> Bet</button>
          </div>
        "
        $("#carousel-inventory").carousel {inverval: false}
        $("#carousel-inventory").carousel 'pause'
        $("#carousel-inventory").on 'slid.bs.carousel', ->
          $(this).carousel 'pause'
          return

        count = 0
        slide = 0
        for name of inventory
          for id in inventory[name]
            if count == 12
              slide += 1
              count = 0
              $("#inventory-modal .modal-body .carousel-inner").append "<div class=\"item\"><div class=\"inventory-wrapper\"><div class=\"inventory\"></div></div></div>"
            $("#inventory-modal .modal-body .carousel-inner .item:last .inventory").append "
              <div data-id=\"" + id + "\" class=\"steam-item " + name + " lg\">
                <div class=\"check\"><i class=\"fa fa-check\"></i></div>
              </div>
            "
            count += 1
        $(".steam-item").off "click"
        $(".steam-item").on "click", ->
          $(this).toggleClass "active"
          if $(".steam-item.active").length > 0
            $(".btn-bet").removeClass "disabled"
          else
            $(".btn-bet").addClass "disabled"
        $(".btn-bet").on "click", ->
          items = []
          $(".steam-item.active").each ->
            items.push $(this).data "id"
          $("#inventory-modal .modal-body").html "
            <p class=\"connection-status\"><i class=\"fa fa-check\"></i> Connected</p>
            <p class=\"inventory-status\"><i class=\"fa fa-check\"></i> Inventory</p>
            <p class=\"bet-status\"><i class=\"fa fa-spin fa-spinner\"></i> Sending tradeoffer</p>
          "
          json = JSON.stringify([
            "bet"
            match
            team
            items
          ])
          socket.send json
          return
      else if array[0] is "tradeOffer"
        if array[1] is false
          $(".bet-status").html "<i class=\"fa fa-times\"></i> Couldn't send the tradeoffer."
        else
          $(".bet-status").html "
            <p><i class=\"fa fa-check\"></i> Tradeoffer</p>
            <div class=\"progress\">
              <div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"100\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 100%\">
              </div>
            </div>
          "
          $("#inventory-modal .modal-body .progress-bar").addClass "countdown"
          setTimeout (->
            $("#inventory-modal .modal-body .progress-bar").css "width", "0%"
            return
          ), 1000
          $("#inventory-modal .modal-body").append "<a class=\"btn btn-block btn-primary btn-tradeoffer\" href=\"http://steamcommunity.com/tradeoffer/" + array[1] + "\" target=\"_blank\"><i class=\"fa fa-refresh\"></i> Trade Offer</a>"    
      else if array[0] is "accepted"
        $(".btn-tradeoffer").remove()
        if array[1] is false
          $(".bet-status").html "<i class=\"fa fa-times\"></i> You were too slow and the time has expired."
        else
          $(".bet-status").html "<i class=\"fa fa-heart\"></i> It was a pleasure to bet with you!"
          callback = ->
            window.open "http://" + window.location.host + "/bet/" + match + "/", "_self"
          setTimeout(callback, 1000)

    $(".btn-inventory").on "click", ->
      team = $(this).data "team"
      match = $(this).data "match"
      return
    $("#inventory-modal").on "show.bs.modal", (e) ->
      $("#inventory-modal .modal-body").html "
        <p class=\"connection-status\">
          <i class=\"fa fa-spinner fa-spin\"></i> Establishing connection with bot
        </p>
      "
      return
    $("#inventory-modal").on "shown.bs.modal", (e) ->
      json = JSON.stringify([
        "hello"
        steamID
      ])
      socket.send json
      return

  return