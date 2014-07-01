%rebase layout user=user, flash=flash

<script type="text/javascript" src="/static/javascripts/menubar.js">
</script>

<div id="menubar">
  <span class="button">
    <a href="/shop/index">Shop</a>
  </span>
  <span class="button">
    <a href="/shop/cart">Carrello</a>
  </span>
  <span class="button">
    <a href="/shop/download_pricelist">Scarica il listino</a>
  </span>
  <span class="button">
    <a href="/user/modify">Modifica registrazione</a>
  </span>
  <span class="button">
    <a href="/shop/support">Supporto</a>
  </span>
  <span class="button">
    <a href="/shop/info">Vendite</a>
  </span>
  <span class="button">
    <a href="/shop/contacts">Contatti</a>
  </span>

% # If the user is an admin user, print the admin button
%if user['admin'] == 't':
  <span class="button">
    <a href="/admin/index">Admin</a>
  </span>
%end

  <span class="button">
    <a href="#" onclick="logout()">Logout</a>
  </span>
</div>

<div id="main">
  %include
  <div class="clearer"></div>
</div>
