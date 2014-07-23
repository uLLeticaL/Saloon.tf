(function() {
  $(function() {
    var bet, bot, loadBets, logElements, logTimers, match, offset, payout, socket, team;
    if (page === "bet") {
      offset = 0;
      loadBets = function() {
        $.getJSON("/api/bet/" + betID + "/bets/offset/" + offset + "/", function(data) {
          var $element, bet, i, itemsGroup, number, _i, _j, _k, _l, _len, _len1, _ref, _ref1, _ref2, _ref3;
          console.log(data);
          for (number in data) {
            bet = data[number];
            $element = $("<div class=\"bet-details panel panel-default animated fadeInUp\"> <div class=\"panel-heading\">" + bet["user"]["name"] + " placed a bet on <strong>" + bet["team"]["name"] + "</strong> </div> <div class=\"panel-body\"> <div class=\"inventory-wrapper\"> <div class=\"inventory\"> </div> </div> </div> </div>");
            if (bet["status"] === 1 || bet["status"] === 2) {
              $element.find(".panel-heading").append(" and won!");
              _ref = bet["wonGroups"];
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                itemsGroup = _ref[_i];
                for (i = _j = 0, _ref1 = itemsGroup[2]; 0 <= _ref1 ? _j < _ref1 : _j > _ref1; i = 0 <= _ref1 ? ++_j : --_j) {
                  $element.find(".inventory").append("<div class=\"steam-item quality-" + itemsGroup[1] + "\" style=\"background-image:url('/images/items/" + itemsGroup[0] + ".png');\"><div class=\"value\">New</div></div>");
                }
              }
            }
            _ref2 = bet["groups"];
            for (_k = 0, _len1 = _ref2.length; _k < _len1; _k++) {
              itemsGroup = _ref2[_k];
              for (i = _l = 0, _ref3 = itemsGroup[2]; 0 <= _ref3 ? _l < _ref3 : _l > _ref3; i = 0 <= _ref3 ? ++_l : --_l) {
                $element.find(".inventory").append("<div class=\"steam-item quality-" + itemsGroup[1] + "\" style=\"background-image:url('/images/items/" + itemsGroup[0] + ".png');\"></div>");
              }
            }
            if ($(".bets-row .col-md-6.left").height() <= $(".bets-row .col-md-6.right").height()) {
              $(".bets-row .col-md-6.left").append($element);
            } else {
              $(".bets-row .col-md-6.right").append($element);
            }
          }
        });
      };
      loadBets();
    }
    if (page === "bet" || page === "home") {
      team = void 0;
      match = void 0;
      bot = void 0;
      bet = false;
      payout = false;
      logTimers = [];
      logElements = [];
      socket = new WebSocket("ws://direct.saloon.tf:9000");
      socket.onopen = function() {
        var json;
        console.log($(".has-panel").length);
        if ($(".has-panel").length > 0) {
          console.log($(".has-panel").length);
          json = JSON.stringify(["tuneIn", betID]);
          socket.send(json);
        }
      };
      socket.onclose = function() {
        $("#inventory-modal").modal("hide");
        $("#payout-modal").modal("hide");
      };
      socket.onmessage = function(event) {
        var $item, array, callback, count, id, inventory, item, itemsGroup, slide, _i, _len, _ref;
        array = JSON.parse(event.data);
        if (array[0] === "log") {
          if (array[1] === "kill") {
            return setTimeout((function() {
              var $element, index, newTimers, player1, player2, timeout, timer, _i, _len;
              newTimers = [];
              for (timer = _i = 0, _len = logTimers.length; _i < _len; timer = ++_i) {
                index = logTimers[timer];
                clearTimeout(timer);
                timeout = setTimeout((function() {
                  logElements[index].find(".logs-kill").addClass("animated fadeOut");
                }), 3000);
                newTimers.push(timeout);
              }
              logTimers = newTimers;
              player1 = array[2];
              player2 = array[3];
              $(".logs .logs-header").after;
              $element = $("<div class=\"list-group-item logs-item\"> <div class=\"logs-kill animated fadeIn\"> <span class=\"logs-player\"> <img class=\"avatar-sm\" src=\"/images/teams/" + player1[0] + ".jpg\"> <span>" + player1[1] + "</span> </span> <span class=\"logs-weapon sprite-killicon-" + array[4] + "\"> <span class=\"sprite-killicon-display\"></span> </span> <span class=\"logs-player\"> <img class=\"avatar-sm\" src=\"/images/teams/" + player2[0] + ".jpg\"> <span>" + player2[1] + "</span> </span> </div> </div>");
              timeout = setTimeout((function() {
                $element.find(".logs-kill").addClass("animated fadeOut");
              }), 3000);
              logTimers.push(timeout);
              logElements.push($element);
              $(".logs .logs-header").after($element);
              return $(".logs .logs-item").last().remove();
            }), 17000);
          } else if (array[1] === "capture") {
            $(".logs .logs-header").after("<div class=\"list-group-item logs-item active\"> <div class=\"logs-capture\"> <img class=\"avatar-sm\" src=\"/images/teams/" + array[2] + ".jpg\">" + teams[array[2]]["name"] + " captured a control point! </div> </div>");
            return $(".logs .logs-item").last().remove();
          }
        } else if (array[0] === "tradeLink") {
          if (array[1] === "new") {
            if (bet) {
              $("#inventory-modal .modal-body").append("<div class=\"form-group tradelink-form\"> <label for=\"tradelink-input\"><i class=\"fa fa-exclamation-circle\"></i> Please paste your tradeoffers link below</label> <input class=\"form-control tradelink-input\" name=\"tradelink-input\"> </div>");
              return $("#inventory-modal .tradelink-input").on("keyup", function(e) {
                var json;
                $(this).parent().removeClass("has-error");
                if (e.which === 13) {
                  json = JSON.stringify(["tradeLink", $(".tradelink-input").val()]);
                  socket.send(json);
                }
              });
            }
          } else if (array[1] === "wrong") {
            return $(".tradelink-form").addClass("has-error");
          }
        } else if (array[0] === "inventory") {
          inventory = array[1];
          $("#inventory-modal .modal-body").html("<div class=\"carousel-inventory-wrapper\"> <div id=\"carousel-inventory\" class=\"carousel slide\"> <div class=\"carousel-inner\"> <div class=\"item active\"><div class=\"inventory-wrapper\"><div class=\"inventory\"></div></div></div> </div> </div> <a class=\"left carousel-inventory-control carousel-control\" href=\"#carousel-inventory\" role=\"button\" data-slide=\"prev\"> <span class=\"fa fa-chevron-left\"></span> </a> <a class=\"right carousel-inventory-control carousel-control\" href=\"#carousel-inventory\" role=\"button\" data-slide=\"next\"> <span class=\"fa fa-chevron-right\"></span> </a> </div> <div class=\"btn-bet-wrapper\"> <button class=\"btn btn-primary btn-bet disabled\"><i class=\"fa fa-gavel\"></i> Bet</button> </div>");
          $("#carousel-inventory").carousel({
            inverval: false
          });
          $("#carousel-inventory").carousel("pause");
          $("#carousel-inventory").on("slid.bs.carousel", function() {
            $(this).carousel("pause");
          });
          count = 0;
          slide = 0;
          $(".steam-item").off("click");
          for (_i = 0, _len = inventory.length; _i < _len; _i++) {
            itemsGroup = inventory[_i];
            _ref = itemsGroup["items"];
            for (id in _ref) {
              item = _ref[id];
              if (count === 12) {
                slide += 1;
                count = 0;
                $("#inventory-modal .carousel-inner").append("<div class=\"item\"><div class=\"inventory-wrapper\"><div class=\"inventory\"></div></div></div>");
              }
              $item = $("<div data-assetid=\"" + id + "\" data-originid=\"" + item["originID"] + "\" class=\"steam-item lg quality-" + itemsGroup["quality"] + "\" style=\"background-image: url(\'/images/items/" + itemsGroup["defindex"] + ".png\')\"> <div class=\"check\"><i class=\"fa fa-check\"></i></div> <span class=\"value\">" + itemsGroup["value"] + "</span> </div>");
              $item.on("click", function() {
                $(this).toggleClass("active");
                if ($(".steam-item.active").length > 0) {
                  return $(".btn-bet").removeClass("disabled");
                } else {
                  return $(".btn-bet").addClass("disabled");
                }
              });
              $("#inventory-modal .inventory").append($item);
              count += 1;
            }
          }
          return $(".btn-bet").on("click", function() {
            var items, json;
            items = [];
            $(".steam-item.active").each(function() {
              return items.push($(this).data("assetid"));
            });
            $("#inventory-modal .modal-body").html("<p class=\"connection-status\"><i class=\"fa fa-check\"></i> Connected</p> <p class=\"inventory-status\"><i class=\"fa fa-check\"></i> Inventory</p> <p class=\"bet-status\"><i class=\"fa fa-spin fa-circle-o-notch\"></i> Sending tradeoffer</p>");
            json = JSON.stringify(["bet", match, team, items]);
            socket.send(json);
          });
        } else if (array[0] === "tradeOffer") {
          if (bet) {
            if (array[1] === false) {
              return $("#inventory-modal .bet-status").html("<i class=\"fa fa-times\"></i> Couldn't send the tradeoffer.");
            } else {
              $("#inventory-modal .bet-status").html("<p><i class=\"fa fa-check\"></i> Tradeoffer</p> <div class=\"progress\"> <div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"100\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 100%\"> </div> </div>");
              $("#inventory-modal .modal-body .progress-bar").addClass("countdown");
              setTimeout((function() {
                $("#inventory-modal .modal-body .progress-bar").css("width", "0%");
              }), 1000);
              return $("#inventory-modal .modal-body").append("<a class=\"btn btn-block btn-primary btn-tradeoffer\" href=\"http://steamcommunity.com/tradeoffer/" + array[1] + "\" target=\"_blank\"><i class=\"fa fa-refresh\"></i> Trade Offer</a>");
            }
          } else if (payout) {
            if (array[1] === false) {
              $(".btn-payout").html("<i class=\"fa fa-times-circle\"></i> Payout");
              return payout = false;
            } else {
              $(".btn-payout").remove();
              $(".heading-won").append("<a href=\"http://steamcommunity.com/tradeoffer/" + array[1] + "\" target=\"_blank\" class=\"btn btn-md btn-primary btn-payout pull-right\"><i class=\"fa fa-refresh\"></i> Trade</a>");
              return payout = false;
            }
          }
        } else if (array[0] === "accepted") {
          if (bet) {
            $(".btn-tradeoffer").remove();
            if (array[1] === false) {
              return $("#inventory-modal .bet-status").html("<i class=\"fa fa-times\"></i> You were too slow and the time has expired.");
            } else {
              $("#inventory-modal .bet-status").html("<i class=\"fa fa-heart\"></i> It was a pleasure to bet with you!");
              callback = function() {
                return window.open("http://" + window.location.host + "/bet/" + match + "/", "_self");
              };
              return setTimeout(callback, 1000);
            }
          }
        } else if (array[0] === "payout") {
          if (array[1] === "error") {
            $(".btn-payout").html("<i class=\"fa fa-times-circle\"></i> Payout");
            return payout = false;
          } else if (array[1] === "processing") {
            return $(".btn-payout").html("<i class=\"fa fa-spin fa-circle-o-notch\"></i> Payout");
          }
        }
      };
      $(".btn-inventory").on("click", function() {
        team = $(this).data("team");
        match = $(this).data("match");
      });
      $("#inventory-modal").on("show.bs.modal", function(e) {
        payout = false;
        bet = true;
        $("#inventory-modal .modal-body").html("<p class=\"connection-status\"> <i class=\"fa fa-circle-o-notch fa-spin\"></i> Establishing connection with bot </p>");
      });
      $("#inventory-modal").on("shown.bs.modal", function(e) {
        var json;
        json = JSON.stringify(["inventory", steamID]);
        socket.send(json);
      });
      $("#inventory-modal").on("hide.bs.modal", function(e) {
        bet = false;
      });
      $(".btn-payout").on("click", function() {
        var bat, json;
        $(".btn-payout").html("<i class=\"fa fa-spin fa-circle-o-notch\"></i> Payout");
        bat = false;
        payout = true;
        json = JSON.stringify(["payout", steamID, betID]);
        socket.send(json);
      });
    }
  });

}).call(this);

(function() {
  $(function() {
    if (page === "home") {
      $(".bet").on("click", function(e) {
        if (!$("button").is(e.target)) {
          window.open("http://" + window.location.host + "/bet/" + $(this).data("id") + "/", "_self");
        }
      });
    }
  });

}).call(this);

(function() {


}).call(this);

(function() {
  $(function() {
    if (page === "manage") {
      if ($(".removeLeague-button").length > 0) {
        $(".removeLeague-button").on("click", function() {
          var id;
          id = $(this).data("id");
          $("#removeLeague-confirm").off("click");
          $("#removeLeague-confirm").on("click", function() {
            $.ajax({
              url: "/manage/leagues/remove/" + id,
              context: document.body
            }).done(function(data) {
              var array;
              array = JSON.parse(data);
              if (array["success"]) {
                window.setTimeout((function() {
                  window.open("http://" + window.location.host + "/manage/leagues", "_self");
                }), 0);
              } else {
                $("#removeLeague-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                window.setTimeout((function() {
                  window.open("http://" + window.location.host + "/manage/leagues", "_self");
                }), 3000);
              }
            });
          });
          $("#removeLeague-modal").modal("show");
        });
      }
      if ($(".editLeague-button").length > 0) {
        $(".editLeague-button").on("click", function() {
          var array;
          array = $(this).data("json");
          $('#editLeague-form [name="name"]').val(array["name"]);
          $('#editLeague-form .btn').removeClass('active');
          $('#editLeague-form [value="' + array["type"] + '"]').prop("checked", true);
          $('#editLeague-form [value="' + array["region"] + '"]').prop("checked", true);
          $('#editLeague-form [value="' + array["type"] + '"]').parent().addClass("active");
          $('#editLeague-form [value="' + array["region"] + '"]').parent().addClass("active");
          $('#editLeague-form [name="accentColour"]').val(array["colour"]);
          $("#editLeague-modal").modal("show");
          $('#editLeague-form').submit(function() {
            $.ajax({
              type: "POST",
              url: "/manage/leagues/edit/" + array["id"] + "/",
              data: $(this).serialize(),
              context: document.body,
              success: function(data) {
                array = JSON.parse(data);
                if (array["success"]) {
                  window.setTimeout((function() {
                    window.open("http://" + window.location.host + "/manage/leagues", "_self");
                  }), 0);
                } else {
                  $("#editLeague-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                  window.setTimeout((function() {
                    window.open("http://" + window.location.host + "/manage/leagues", "_self");
                  }), 3000);
                }
              }
            });
            return false;
          });
        });
      }
      if ($(".removeTeam-button").length > 0) {
        $(".removeTeam-button").on("click", function() {
          var id;
          id = $(this).data("id");
          $("#removeTeam-confirm").off("click");
          $("#removeTeam-confirm").on("click", function() {
            $.ajax({
              url: location.href + "remove/" + id + "/",
              context: document.body
            }).done(function(data) {
              var array;
              array = JSON.parse(data);
              if (array["success"]) {
                window.setTimeout((function() {
                  window.open(location.href, "_self");
                }), 0);
              } else {
                $("#removeTeam-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                window.setTimeout((function() {
                  window.open(location.href, "_self");
                }), 3000);
              }
            });
          });
          $("#removeTeam-modal").modal("show");
        });
      }
      if ($(".editTeam-button").length > 0) {
        $(".editTeam-button").on("click", function() {
          var array;
          array = $(this).data("json");
          $('#editTeam-form [name="name"]').val(array["name"]);
          $('#editTeam-form [name="leagueID"]').val(array["leagueID"]);
          $('#editTeam-form [name="country"]').val(array["countryID"]);
          $("#editTeam-modal").modal("show");
          $('#editTeam-form').submit(function() {
            $.ajax({
              type: "POST",
              url: location.href + "edit/" + array["id"] + "/",
              data: $(this).serialize(),
              context: document.body,
              success: function(data) {
                array = JSON.parse(data);
                if (array["success"]) {
                  window.setTimeout((function() {
                    window.open(location.href, "_self");
                  }), 0);
                } else {
                  $("#editTeam-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                  window.setTimeout((function() {
                    window.open(location.href, "_self");
                  }), 3000);
                }
              }
            });
            return false;
          });
        });
      }
      if ($(".removeMatch-button").length > 0) {
        $(".removeMatch-button").on("click", function() {
          var id;
          id = $(this).data("id");
          $("#removeMatch-confirm").off("click");
          $("#removeMatch-confirm").on("click", function() {
            $.ajax({
              url: location.href + "remove/" + id + "/",
              context: document.body
            }).done(function(data) {
              var array;
              array = JSON.parse(data);
              if (array["success"]) {
                window.setTimeout((function() {
                  window.open(location.href, "_self");
                }), 0);
              } else {
                $("#removeMatch-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                window.setTimeout((function() {
                  window.open(location.href, "_self");
                }), 3000);
              }
            });
          });
          $("#removeMatch-modal").modal("show");
        });
      }
      if ($(".editMatch-button").length > 0) {
        $(".editMatch-button").on("click", function() {
          var array;
          array = $(this).data("json");
          console.log(array);
          $('#editMatch-form [name="team1"]').val(array["team1"]["id"]);
          $('#editMatch-form [name="team2"]').val(array["team2"]["id"]);
          $('#editMatch-form [name="channel"]').val(array["channel"]);
          $('#editMatch-form [name="ip"]').val(array["ip"]);
          $('#editMatch-form [name="port"]').val(array["port"]);
          $('#editMatch-form [name="rcon"]').val(array["rcon"]);
          $('#editMatch-form [name="logsecret"]').val(array["logsecret"]);
          $("#editMatch-modal").modal("show");
          $('#editMatch-form').submit(function() {
            $.ajax({
              type: "POST",
              url: location.href + "edit/" + array["id"] + "/",
              data: $(this).serialize(),
              context: document.body,
              success: function(data) {
                array = JSON.parse(data);
                if (array["success"]) {
                  window.setTimeout((function() {
                    window.open(location.href, "_self");
                  }), 0);
                } else {
                  $("#editMatch-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                  window.setTimeout((function() {
                    window.open(location.href, "_self");
                  }), 3000);
                }
              }
            });
            return false;
          });
        });
      }
      if ($("#user-search").length > 0) {
        return $("#user-search").on("keyup", function() {
          if ($("#user-search").val().length) {
            $.getJSON("/api/users/name/" + $("#user-search").val() + "/limit/5/", function(data) {
              var player, _i, _len, _results;
              if ($(".search .list-group").length === 0) {
                $(".search").append("<div class=\"list-group\"></div>");
              } else {
                $(".search .list-group").empty();
              }
              _results = [];
              for (_i = 0, _len = data.length; _i < _len; _i++) {
                player = data[_i];
                _results.push($(".search .list-group").append("<a class=\"list-group-item\" href=\"/manage/users/" + player["id"] + "/\"><i class=\"fa fa-user\"></i> " + player["name"] + "</a>"));
              }
              return _results;
            });
          } else {
            $(".search .list-group").remove();
          }
        });
      }
    }
  });

  return;

}).call(this);
