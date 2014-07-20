<%namespace name="partials" file="partials.mako"/>
<%inherit file="/base.mako" />
<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>
%for bet in c.bets:
  ${partials.bet(bet["match"])}
%endfor