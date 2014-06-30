var fs = require('fs');
var colors = require('colors');
var Steam = require('steam');

var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:9000');
ws.on('open', function() {
  console.log("[WebSocket]".cyan, "Connected successfully");
  ws.on('message', function(message) {
    console.log("[WebSocket]".cyan, "Message:", message);
    array = JSON.parse(message);
    if (array[0] == "bot") {
      if (array.length == 2) {
        Bot(array[1]);
      }
      else {
        Bot(array[1], array[2]);
      }
    }
  });
});
ws.on('close', function() {
  console.log("[WebSocket]".cyan, "Disconnected");
  process.exit()
});

function Bot(data, authCode) {
  if (fs.existsSync('servers')) {
    Steam.servers = JSON.parse(fs.readFileSync('servers'));
  }

  var bot = new Steam.SteamClient();
  var options = {
    accountName: data.steamLogin,
    password: data.steamPassword
  }
  if (fs.existsSync('sentry/' + data.steamLogin) || authCode) {
    if (authCode) {
      options["authCode"] = authCode;
    }
    else {
      options["shaSentryfile"] = fs.readFileSync('sentry/' + data.steamLogin);
    }
    bot.logOn(options);

    bot.on('sentry', function(sentryHash) {
      fs.writeFile('sentry/' + data.steamLogin, sentryHash, function(err) {
        if (err)
          console.log(("[" + data.name + "]").cyan, 'Error opening sentry file: ', err);
        else
          console.log("[" + data.name + "]".cyan, 'Saved sentry file hash as "sentry/' + data.steamLogin + '"');
      });
    });

    bot.on('loggedOn', function() {
      bot.setPersonaState(Steam.EPersonaState.Online);
      console.log(("[" + data.name + "]").cyan, "Logged in successfully")
    });

    bot.on('servers', function(servers) {
      fs.writeFile('servers', JSON.stringify(servers));
    });

    bot.on('tradeOffers', function(number) {
      if (number > 0) {
        console.log(("[" + data.name + "]").cyan, "Got a trade offer");
        ws.send('["tradeOffers",' + data.id + ']')
      }
    }); 
  }
  else {
    var domain = require('domain').create();
    domain.on('error', function(err) {
      if (err.eresult == 63) {
        console.log(("[" + data.name + "]").cyan, "Need SteamGuard code");
        ws.send('["guardCode",' + data.id + ']');
      }
      else {
        throw err;
      }
    });
    domain.run( function () {
      bot.logOn(options);
    });
  }
}