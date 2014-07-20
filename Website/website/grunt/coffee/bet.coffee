$ ->
  if page is "bet"
    offset = 0
    loadBets = ->
      $.getJSON "/api/bet/" + betID + "/bets/offset/" + offset + "/", (data) ->
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
          if bet["status"] is 1 or bet["status"] is 2
            $element.find(".panel-heading").append " and won!"
            for itemsGroup in bet["wonGroups"]
              for i in [0...itemsGroup[2]]
                $element.find(".inventory").append "
                  <div class=\"steam-item quality-" + itemsGroup[1] + "\" style=\"background-image:url('/images/items/" + itemsGroup[0] + ".png');\"><div class=\"value\">New</div></div>
                "
          for itemsGroup in bet["groups"]
            for i in [0...itemsGroup[2]]
              $element.find(".inventory").append "
                <div class=\"steam-item quality-" + itemsGroup[1] + "\" style=\"background-image:url('/images/items/" + itemsGroup[0] + ".png');\"></div>
              "
          if $(".bets-row .col-md-6.left").height() <= $(".bets-row .col-md-6.right").height()
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
    bet = false
    payout = false
    socket = new WebSocket("ws://direct.saloon.tf:9000")

    socket.onopen = ->
      return

    socket.onclose = ->
      $("#inventory-modal").modal "hide"
      $("#payout-modal").modal "hide"
      return

    socket.onmessage = (event) ->
      array = JSON.parse(event.data)
      console.log array
      if array[0] is "tradeLink"
        if array[1] is "new"
          if bet
            $("#inventory-modal .modal-body").append "
              <div class=\"form-group tradelink-form\">
                <label for=\"tradelink-input\"><i class=\"fa fa-exclamation-circle\"></i> Please paste your tradeoffers link below</label>
                  <input class=\"form-control tradelink-input\" name=\"tradelink-input\">
              </div>
            "
            $("#inventory-modal .tradelink-input").on "keyup", (e) ->
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
        $(".steam-item").off "click"

        for itemsGroup in inventory
          for id, item of itemsGroup["items"]
            if count == 12
              slide += 1
              count = 0
              $("#inventory-modal .carousel-inner").append "<div class=\"item\"><div class=\"inventory-wrapper\"><div class=\"inventory\"></div></div></div>"
            $item = $ "
              <div data-assetid=\"" + id + "\" data-originid=\"" + item["originID"] + "\" class=\"steam-item lg quality-" + itemsGroup["quality"] + "\" style=\"background-image: url(\'/images/items/" + itemsGroup["defindex"] + ".png\')\">
                <div class=\"check\"><i class=\"fa fa-check\"></i></div>
                <span class=\"value\">" + itemsGroup["value"] + "</span>
              </div>
            "

            $item.on "click", ->
              $(this).toggleClass "active"
              if $(".steam-item.active").length > 0
                $(".btn-bet").removeClass "disabled"
              else
                $(".btn-bet").addClass "disabled"

            $("#inventory-modal .inventory").append $item
            count += 1

        $(".btn-bet").on "click", ->
          items = []
          $(".steam-item.active").each ->
            items.push $(this).data("assetid")

          $("#inventory-modal .modal-body").html "
            <p class=\"connection-status\"><i class=\"fa fa-check\"></i> Connected</p>
            <p class=\"inventory-status\"><i class=\"fa fa-check\"></i> Inventory</p>
            <p class=\"bet-status\"><i class=\"fa fa-spin fa-circle-o-notch\"></i> Sending tradeoffer</p>
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
        if bet
          if array[1] is false
            $("#inventory-modal .bet-status").html "<i class=\"fa fa-times\"></i> Couldn't send the tradeoffer."
          else
            $("#inventory-modal .bet-status").html "
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
        else if payout
          if array[1] is false
            $(".btn-payout").html "<i class=\"fa fa-times-circle\"></i> Payout"
            payout = false
          else
            $(".btn-payout").remove()
            $(".heading-won").append "<a href=\"http://steamcommunity.com/tradeoffer/" + array[1] + "\" target=\"_blank\" class=\"btn btn-md btn-primary btn-payout pull-right\"><i class=\"fa fa-refresh\"></i> Trade</a>"
            payout = false

      else if array[0] is "accepted"
        if bet
          $(".btn-tradeoffer").remove()
          if array[1] is false
            $("#inventory-modal .bet-status").html "<i class=\"fa fa-times\"></i> You were too slow and the time has expired."
          else
            $("#inventory-modal .bet-status").html "<i class=\"fa fa-heart\"></i> It was a pleasure to bet with you!"
            callback = ->
              window.open "http://" + window.location.host + "/bet/" + match + "/", "_self"
            setTimeout(callback, 1000)
      else if array[0] is "payout"
        if array[1] is "error"
          $(".btn-payout").html "<i class=\"fa fa-times-circle\"></i> Payout"
          payout = false
        else if array[1] is "processing"
          $(".btn-payout").html "<i class=\"fa fa-spin fa-circle-o-notch\"></i> Payout"

    $(".btn-inventory").on "click", ->
      team = $(this).data "team"
      match = $(this).data "match"
      return
    $("#inventory-modal").on "show.bs.modal", (e) ->
      payout = false
      bet = true
      $("#inventory-modal .modal-body").html "
        <p class=\"connection-status\">
          <i class=\"fa fa-circle-o-notch fa-spin\"></i> Establishing connection with bot
        </p>
      "
      return
    $("#inventory-modal").on "shown.bs.modal", (e) ->
      json = JSON.stringify([
        "inventory"
        steamID
      ])
      socket.send json
      return
    $("#inventory-modal").on "hide.bs.modal", (e) ->
      bet = false
      return

    $(".btn-payout").on "click", ->
      $(".btn-payout").html "<i class=\"fa fa-spin fa-circle-o-notch\"></i> Payout"
      bat = false
      payout = true
      json = JSON.stringify([
        "payout"
        steamID,
        betID
      ])
      socket.send json
      return

  return