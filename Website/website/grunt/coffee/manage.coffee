$ ->
  if page is "manage"
    if $(".removeLeague-button").length > 0
      $(".removeLeague-button").on "click", ->
        id = $(this).data("id")
        $("#removeLeague-confirm").off "click"
        $("#removeLeague-confirm").on "click", ->
          $.ajax(
            url: "/manage/leagues/remove/" + id
            context: document.body
          ).done (data) ->
            array = JSON.parse(data)
            if array["success"]
              window.setTimeout (->
                window.open "http://"  + window.location.host + "/manage/leagues", "_self"
                return
              ), 0
            else
              $("#removeLeague-modal .modal-body").html "<p class=\"text-danger\">" + array["message"] + "</p>"
              window.setTimeout (->
                window.open "http://"  + window.location.host + "/manage/leagues", "_self"
                return
              ), 3000
            return
          return
        $("#removeLeague-modal").modal "show"
        return
    if $(".editLeague-button").length > 0
      $(".editLeague-button").on "click", ->
        array = $(this).data("json")
        $('#editLeague-form [name="name"]').val array["name"]
        $('#editLeague-form .btn').removeClass 'active'
        $('#editLeague-form [value="' + array["type"] + '"]').prop "checked", true
        $('#editLeague-form [value="' + array["region"] + '"]').prop "checked", true
        $('#editLeague-form [value="' + array["type"] + '"]').parent().addClass "active"
        $('#editLeague-form [value="' + array["region"] + '"]').parent().addClass "active"
        $('#editLeague-form [name="accentColour"]').val array["colour"]
        $("#editLeague-modal").modal "show"
        $('#editLeague-form').submit ->
          $.ajax(
            type: "POST"
            url: "/manage/leagues/edit/" + array["id"] + "/"
            data: $(this).serialize()
            context: document.body
            success: (data) ->
              array = JSON.parse(data)
              if array["success"]
                window.setTimeout (->
                  window.open "http://"  + window.location.host + "/manage/leagues", "_self"
                  return
                ), 0
              else
                $("#editLeague-modal .modal-body").html "<p class=\"text-danger\">" + array["message"] + "</p>"
                window.setTimeout (->
                  window.open "http://"  + window.location.host + "/manage/leagues", "_self"
                  return
                ), 3000
              return
          )
          false
        return
    if $(".removeTeam-button").length > 0
      $(".removeTeam-button").on "click", ->
        id = $(this).data("id")
        $("#removeTeam-confirm").off "click"
        $("#removeTeam-confirm").on "click", ->
          $.ajax(
            url: location.href + "remove/" + id + "/"
            context: document.body
          ).done (data) ->
            array = JSON.parse(data)
            if array["success"]
              window.setTimeout (->
                window.open location.href, "_self"
                return
              ), 0
            else
              $("#removeTeam-modal .modal-body").html "<p class=\"text-danger\">" + array["message"] + "</p>"
              window.setTimeout (->
                window.open location.href, "_self"
                return
              ), 3000
            return
          return
        $("#removeTeam-modal").modal "show"
        return
    if $(".editTeam-button").length > 0
      $(".editTeam-button").on "click", ->
        array = $(this).data("json")
        $('#editTeam-form [name="name"]').val array["name"]
        $('#editTeam-form [name="leagueID"]').val array["leagueID"]
        $('#editTeam-form [name="country"]').val array["countryID"]
        $("#editTeam-modal").modal "show"
        $('#editTeam-form').submit ->
          $.ajax(
            type: "POST"
            url: location.href + "edit/" + array["id"] + "/"
            data: $(this).serialize()
            context: document.body
            success: (data) ->
              array = JSON.parse(data)
              if array["success"]
                window.setTimeout (->
                  window.open location.href, "_self"
                  return
                ), 0
              else
                $("#editTeam-modal .modal-body").html "<p class=\"text-danger\">" + array["message"] + "</p>"
                window.setTimeout (->
                  window.open location.href, "_self"
                  return
                ), 3000
              return
          )
          false
        return
    if $(".removeMatch-button").length > 0
      $(".removeMatch-button").on "click", ->
        id = $(this).data("id")
        $("#removeMatch-confirm").off "click"
        $("#removeMatch-confirm").on "click", ->
          $.ajax(
            url: location.href + "remove/" + id + "/"
            context: document.body
          ).done (data) ->
            array = JSON.parse(data)
            if array["success"]
              window.setTimeout (->
                window.open location.href, "_self"
                return
              ), 0
            else
              $("#removeMatch-modal .modal-body").html "<p class=\"text-danger\">" + array["message"] + "</p>"
              window.setTimeout (->
                window.open location.href, "_self"
                return
              ), 3000
            return
          return
        $("#removeMatch-modal").modal "show"
        return

    if $(".editMatch-button").length > 0
      $(".editMatch-button").on "click", ->
        array = $(this).data("json")
        $('#editMatch-form [name="team1"]').val array["team1"]["id"]
        $('#editMatch-form [name="team2"]').val array["team2"]["id"]
        $('#editMatch-form [name="stream"]').val array["stream"]
        $("#editMatch-modal").modal "show"
        $('#editMatch-form').submit ->
          $.ajax(
            type: "POST"
            url: location.href + "edit/" + array["id"] + "/"
            data: $(this).serialize()
            context: document.body
            success: (data) ->
              array = JSON.parse(data)
              if array["success"]
                window.setTimeout (->
                  window.open location.href, "_self"
                  return
                ), 0
              else
                $("#editMatch-modal .modal-body").html "<p class=\"text-danger\">" + array["message"] + "</p>"
                window.setTimeout (->
                  window.open location.href, "_self"
                  return
                ), 3000
              return
          )
          false
        return

    if $("#user-search").length > 0
      $("#user-search").on "keyup", ->
        if $("#user-search").val().length
          $.getJSON "/api/users/name/" + $("#user-search").val() + "/limit/5/", (data) ->
            if $(".search .list-group").length == 0
              $(".search").append "<div class=\"list-group\"></div>"
            else
              $(".search .list-group").empty()
            for player in data
              $(".search .list-group").append("<a class=\"list-group-item\" href=\"/manage/users/" + player["id"] + "/\"><i class=\"fa fa-user\"></i> " + player["name"] + "</a>")
        else
          $(".search .list-group").remove()
        return
return