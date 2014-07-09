var fs = require('fs');
var colors = require('colors');
var Steam = require('steam');

var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:9000');

function Log(name, message) {
  console.log(("[" + name + "]").cyan, message);
  ws.send('["log", "' + name + '", "' + message + '"]');
}

ws.on('open', function() {
  Log("WebSocket", "Connected successfully");
  ws.on('message', function(message) {
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
  console.log(("[WebSocket]").cyan, "Disconnected");
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
          Log(data.name, 'Error opening sentry file: ' + err);
        else
          Log(data.name, "Saved sentry file hash as \"sentry/" + data.steamLogin + "\"");
      });
    });

    bot.on('loggedOn', function() {
      bot.setPersonaState(Steam.EPersonaState.Online);
      Log(data.name, "Logged in successfully")
    });

    bot.on('servers', function(servers) {
      fs.writeFile('servers', JSON.stringify(servers));
    });
    bot.on('friend', function(steamID, relationship) {
      ws.send('["friend", "' + steamID + '", ' + relationship + ']')
    });
  }
  else {
    var domain = require('domain').create();
    domain.on('error', function(err) {
      if (err.eresult == 63) {
        Log(data.name, "Need SteamGuard code");
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