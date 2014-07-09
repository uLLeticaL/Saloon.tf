(function() {
  $(function() {
    var bot, match, openConnection, socket, team;
    if (page === "home" || page === "bet") {
      socket = void 0;
      team = void 0;
      match = void 0;
      bot = void 0;
      openConnection = function(type) {
        $("#" + type + "-modal .modal-body").html("<p class=\"connection-status\"> <i class=\"fa fa-spinner fa-spin\"></i> Establishing connection with bot </p>");
        socket = new WebSocket("ws://direct." + window.location.host + ":9000");
        socket.onopen = function() {
          var json;
          json = JSON.stringify(["hello", steamID]);
          socket.send(json);
        };
        socket.onclose = function() {
          $("#" + type + "-modal").modal("hide");
        };
        return socket.onmessage = function(event) {
          var array, callback, count, id, inventory, name, slide, _i, _len, _ref;
          array = JSON.parse(event.data);
          console.log(array);
          $(".connection-status").html("<i class=\"fa fa-check\"></i> Connected");
          if (array[0] === "hello") {
            bot = array[1];
            $(".connection-status").html("<i class=\"fa fa-check\"></i> Connected");
            $("#" + type + "-modal .modal-body").append("<p class=\"authentication-status\"> <i class=\"fa fa-exclamation-circle\"></i> Bot sent you an invintation</a> </p>");
          } else if (array[0] === "tradeLink") {
            if (array[1] === "new") {
              $("#" + type + "-modal .modal-body").append("<div class=\"form-group tradelink-form\"> <label for=\"tradelink-input\"><i class=\"fa fa-exclamation-circle\"></i> Please paste your tradeoffers link below</label> <input class=\"form-control tradelink-input\" name=\"tradelink-input\"> </div>");
              $(".tradelink-input").on("keyup", function(e) {
                var json;
                $(this).parent().removeClass("has-error");
                if (e.which === 13) {
                  json = JSON.stringify(["tradeLink", $(".tradelink-input").val()]);
                  socket.send(json);
                }
              });
            } else if (array[1] === "wrong") {
              $(".tradelink-form").addClass("has-error");
            }
          } else if (array[0] === "inventory") {
            inventory = array[1];
            $("#inventory-modal .modal-body").html("<div class=\"carousel-inventory-wrapper\"> <div id=\"carousel-inventory\" class=\"carousel slide\"> <div class=\"carousel-inner\"> <div class=\"item active\"><div class=\"inventory-wrapper\"><div class=\"inventory\"></div></div></div> </div> </div> <a class=\"left carousel-inventory-control carousel-control\" href=\"#carousel-inventory\" role=\"button\" data-slide=\"prev\"> <span class=\"fa fa-chevron-left\"></span> </a> <a class=\"right carousel-inventory-control carousel-control\" href=\"#carousel-inventory\" role=\"button\" data-slide=\"next\"> <span class=\"fa fa-chevron-right\"></span> </a> </div> <div class=\"btn-bet-wrapper\"> <button class=\"btn btn-primary btn-bet disabled\"><i class=\"fa fa-gavel\"></i> Bet</button> </div>");
            $("#carousel-inventory").carousel({
              inverval: false
            });
            $("#carousel-inventory").carousel('pause');
            $("#carousel-inventory").on('slid.bs.carousel', function() {
              $(this).carousel('pause');
            });
            count = 0;
            slide = 0;
            for (name in inventory) {
              _ref = inventory[name];
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                id = _ref[_i];
                if (count === 12) {
                  slide += 1;
                  count = 0;
                  $("#inventory-modal .modal-body .carousel-inner").append("<div class=\"item\"><div class=\"inventory-wrapper\"><div class=\"inventory\"></div></div></div>");
                }
                $("#inventory-modal .modal-body .carousel-inner .item:last .inventory").append("<div data-id=\"" + id + "\" class=\"steam-item " + name + "\"> <div class=\"check\"><i class=\"fa fa-check\"></i></div> <img src=\"/images/items/" + name + ".png\"> </div>");
                count += 1;
              }
            }
            $(".steam-item").off("click");
            $(".steam-item").on("click", function() {
              $(this).toggleClass("active");
              if ($(".steam-item.active").length > 0) {
                return $(".btn-bet").removeClass("disabled");
              } else {
                return $(".btn-bet").addClass("disabled");
              }
            });
            $(".btn-bet").on("click", function() {
              var items, json;
              items = [];
              $(".steam-item.active").each(function() {
                return items.push($(this).data("id"));
              });
              $("#inventory-modal .modal-body").html("<p class=\"connection-status\"><i class=\"fa fa-check\"></i> Connected</p> <p class=\"inventory-status\"><i class=\"fa fa-check\"></i> Inventory</p> <p class=\"bet-status\"><i class=\"fa fa-spin fa-spinner\"></i> Sending tradeoffer</p>");
              json = JSON.stringify(["bet", match, team, items]);
              socket.send(json);
            });
          } else if (array[0] === "tradeOffer") {
            if (array[1] === false) {
              $(".bet-status").html("<i class=\"fa fa-times\"></i> Couldn't send the tradeoffer.");
            } else {
              $(".bet-status").html("<p><i class=\"fa fa-check\"></i> Tradeoffer</p> <div class=\"progress\"> <div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"100\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 100%\"> </div> </div>");
              $("#inventory-modal .modal-body .progress-bar").addClass("countdown");
              setTimeout((function() {
                $("#inventory-modal .modal-body .progress-bar").css("width", "0%");
              }), 1000);
              $("#inventory-modal .modal-body").append("<a class=\"btn btn-block btn-primary btn-tradeoffer\" href=\"http://steamcommunity.com/tradeoffer/" + array[1] + "\" target=\"_blank\"><i class=\"fa fa-refresh\"></i> Trade Offer</a>");
            }
          } else if (array[0] === "accepted") {
            $(".btn-tradeoffer").remove;
            if (array[1] === false) {
              $(".bet-status").html("<i class=\"fa fa-times\"></i> You were too slow and the time has expired.");
            } else {
              $(".bet-status").html("<i class=\"fa fa-heart\"></i> It was a pleasure to bet with you!");
              callback = function() {
                return window.open("http://" + window.location.host + "/bet/" + match + "/", "_self");
              };
              setTimeout(callback, 1000);
            }
          }
        };
      };
      $(".btn-inventory").on("click", function() {
        team = $(this).data("team");
        match = $(this).data("match");
      });
      $("#inventory-modal").on("shown.bs.modal", function(e) {
        openConnection("inventory");
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
  var openConnection, socket;

  socket = void 0;

  openConnection = function(type) {
    $("#" + type + "-modal .modal-body").html("<p class=\"connection-status\"> <i class=\"fa fa-spinner fa-spin\"></i> Establishing connection with bot </p>");
    socket = new WebSocket("ws://direct." + window.location.host + ":9000");
    socket.onopen = function() {
      var json;
      $(".connection-status").html("<i class=\"fa fa-check\"></i> Connected");
      $("#" + type + "-modal .modal-body").append("<p class=\"authentication-status\"> <i class=\"fa fa-spinner fa-spin\"></i> Authenticating </p>");
      json = JSON.stringify(["helloOld", type, steamID]);
      socket.send(json);
    };
    socket.onclose = function() {
      $("#" + type + "-modal").modal("hide");
    };
    socket.onmessage = function(event) {
      var array, botArray, queueArray, suffix;
      array = JSON.parse(event.data);
      console.log(array);
      if (array[0] === "helloOld") {
        botArray = array.slice(0);
        $(".authentication-status").html("<i class=\"fa fa-check\"></i> Authenticated");
        if (type === "deposit") {
          $("#deposit-modal .modal-body").append("<p> <i class=\"fa fa-question\"></i> Select items that you want to deposit from your inventory and press accept. </p>");
        } else if (type === "withdraw") {
          if ($(".queue-status").length > 0) {
            $(".queue-status").remove();
          }
          $("#withdraw-modal .modal-body").append("<p> <i class=\"fa fa-question\"></i> Select items that you want to withdraw from bots inventory and press accept. </p>");
        }
        $("#" + type + "-modal .modal-body").append("<p class=\"button-paragraph\"> <button id=\"trade-button\" class=\"btn btn-md btn-primary btn-block\"> <i class=\"fa fa-exchange\"></i> Trade </button> </p>");
        $("#" + type + "-modal .modal-body #trade-button").on("click", function() {
          window.open("/trade/" + botArray[1] + "/", "_blank");
          $("#" + type + "-modal .modal-body .button-paragraph").remove();
          if (type === "deposit") {
            $("#deposit-modal .modal-body").append("<p class=\"trade-status\"> <i class=\"fa fa-spinner fa-spin\"></i> Waiting for trade to be processed </p>");
          }
        });
        if (type === "withdraw") {
          $("#withdraw-modal .modal-body").append("<div class=\"progress\"> <div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"100\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: 100%\"> </div> </div>");
          $("#withdraw-modal .modal-body .progress-bar").addClass("countdown");
          setTimeout((function() {
            $("#withdraw-modal .modal-body .progress-bar").css("width", "0%");
          }), 1000);
        }
      } else if (array[0] === "queue") {
        queueArray = array.slice(0);
        if (queueArray[1] === "position") {
          suffix = (queueArray[2] | 0) % 100;
          suffix = (suffix > 3 && suffix < 21 ? "th" : ["th", "st", "nd", "rd"][suffix % 10] || "th");
          if ($(".queue-status").length > 0) {
            $(".queue-status").html("<i class=\"fa fa-users\"></i> You&rsquo;re " + queueArray[2] + suffix + " in the queue.");
          } else {
            $(".authentication-status").html("<i class=\"fa fa-check\"></i> Authenticated");
            $("#withdraw-modal .modal-body").append("<p class=\"queue-status\"> <i class=\"fa fa-spinner fa-spin\"></i> You&rsquo;re " + queueArray[2] + suffix + " in the queue. </p>");
          }
        }
      } else if (array[0] === "accepted") {
        $(".trade-status").html("<i class=\"fa fa-check\"></i> Trade completed!");
        window.setTimeout((function() {
          window.open("/inventory/", "_self");
        }), 3000);
      } else if (array[0] === "declined") {
        $(".trade-status").html("<i class=\"fa fa-times\"></i> There was an error in the trade.");
        window.setTimeout((function() {
          window.open("/inventory/", "_self");
        }), 3000);
      }
    };
  };

  $(function() {
    if (page === "inventory") {
      $("#deposit-modal").on("shown.bs.modal", function(e) {
        openConnection("deposit");
      });
      $("#deposit-modal").on("hidden.bs.modal", function(e) {
        socket.close();
      });
      $("#withdraw-modal").on("shown.bs.modal", function(e) {
        openConnection("withdraw");
      });
      $("#withdraw-modal").on("hidden.bs.modal", function(e) {
        socket.close();
      });
    }
  });

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
          $('#editMatch-form [name="team1"]').val(array["team1"]["id"]);
          $('#editMatch-form [name="team2"]').val(array["team2"]["id"]);
          $('#editMatch-form [name="stream"]').val(array["stream"]);
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
