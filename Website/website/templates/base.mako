<!DOCTYPE html>
<html>
  <head>
    ${self.head_tags()}
    <script type="text/javascript">
      var page = "${c.current}";
      %if c.user:
        var steamID = "${c.user["steamid"]}";
      %endif
    </script>
    <link rel="shortcut icon" href="/favicon.ico">
    <link rel="icon" href="/favicon.ico">
    <link href='http://fonts.googleapis.com/css?family=Lato:400,700' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" type="text/css" href="/stylesheet.css?v=0.2.322" />
  </head>
  <body class="${c.current}">
    <header>
        <img src="/images/logo.png">
    </header>
    <nav class="navbar navbar-default" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#top-navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
        <div class="collapse navbar-collapse" id="top-navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="${'active' if c.current == "home" else ''}"><a href="/home/">Home</a></li>
            %if c.user:
              %if c.user["permissions"].manage:
                <li class="${'active' if c.current == "manage" else ''}"><a href="/manage/">Manage</a></li>
              %endif
            %endif
          </ul>
          <ul class="nav navbar-nav navbar-right">
            %if c.user:
              <li><a href="/logout/">${c.user["name"]}</a></li>
            %else:
              <li><a href="/login/">Login</a></li>
            %endif
          </ul>
        </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>
    ${self.body()}
    <script type="text/javascript" src="/javascript.js?v=0.2.322" /></script>
  </body>
</html>