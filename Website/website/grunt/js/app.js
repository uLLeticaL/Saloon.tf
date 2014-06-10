(function() {
  $(function() {
    if (page === "home") {
      $(".bet").on("click", function(e) {
        if (!$("button").is(e.target)) {
          window.open("http://saloon.tf/bet/" + $(this).data("id") + "/", "_self");
        }
      });
    }
  });

}).call(this);

(function() {
  var openConnection, socket;

  openConnection = function(type) {
    var socket;
    $("#" + type + "-modal .modal-body").html("<p class=\"connection-status\"> <i class=\"fa fa-spinner fa-spin\"></i> Establishing connection with bot </p>");
    socket = new WebSocket("ws://saloon.tf:9000");
    socket.onopen = function() {
      var json;
      $(".connection-status").html("<i class=\"fa fa-check\"></i> Connected");
      $("#" + type + "-modal .modal-body").append("<p class=\"authentication-status\"> <i class=\"fa fa-spinner fa-spin\"></i> Authenticating </p>");
      json = JSON.stringify(["hello", type, steamID]);
      socket.send(json);
    };
    socket.onclose = function() {
      $("#" + type + "-modal").modal("hide");
    };
    socket.onmessage = function(event) {
      var array, botArray, queueArray, suffix;
      array = JSON.parse(event.data);
      console.log(array);
      if (array[0] === "hello") {
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
          window.open("http://saloon.tf/trade/" + botArray[1] + "/", "_blank");
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
          window.open("http://saloon.tf/inventory/", "_self");
        }), 3000);
      } else if (array[0] === "declined") {
        $(".trade-status").html("<i class=\"fa fa-times\"></i> There was an error in the trade.");
        window.setTimeout((function() {
          window.open("http://saloon.tf/inventory/", "_self");
        }), 3000);
      }
    };
  };

  socket = void 0;

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
                  window.open("http://saloon.tf/manage/leagues", "_self");
                }), 0);
              } else {
                $("#removeLeague-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                window.setTimeout((function() {
                  window.open("http://saloon.tf/manage/leagues", "_self");
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
            console.log($(this).serialize());
            $.ajax({
              type: "POST",
              url: "/manage/leagues/edit/" + array["id"] + "/",
              data: $(this).serialize(),
              context: document.body,
              success: function(data) {
                array = JSON.parse(data);
                if (array["success"]) {
                  window.setTimeout((function() {
                    window.open("http://saloon.tf/manage/leagues", "_self");
                  }), 0);
                } else {
                  $("#editLeague-modal .modal-body").html("<p class=\"text-danger\">" + array["message"] + "</p>");
                  window.setTimeout((function() {
                    window.open("http://saloon.tf/manage/leagues", "_self");
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
          console.log(1);
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
                console.log(location.href + "edit/" + array["id"] + "/");
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
    }
  });

}).call(this);
