$ ->
  if page is "home"
    $(".bet").on "click", (e) ->
      window.open "http://" + window.location.host + "/bet/" + $(this).data("id") + "/", "_self"  unless $("button").is(e.target)
      return
  return