<%inherit file="/base.mako" />

<%def name="head_tags()">
  <script type="text/javascript">
    window.open( "${c.url}", "_self" );
  </script>
</%def>

<div class="container">
  <div class="well">
    <p><i class="fa fa-exclamation-triangle"></i> You must have pop ups enabled to send trade offer.</p>
  </div>
</div>