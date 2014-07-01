%rebase layout user=user, flash=flash, admin=1

<script type="text/javascript" src="/static/javascripts/menubar.js">
</script>

<div id="menubar">
  <span class="button">
    <a href="/admin/index">Categorie</a>
  </span>
  <span class="button">
    <a href="/admin/items">Articoli</a>
  </span>
  <span class="button">
    <a href="/admin/users">Utenti</a>
  </span>
  <span class="button">
    <a href="/admin/pricelists">Listini</a>
  </span>
  <span class="button">
    <a href="/admin/promo">Promo</a>
  </span>
  <span class="button">
    <a href="/shop/index">Shop</a>
  </span>
  <span class="button">
    <a href="#" onclick="logout()">Logout</a>
  </span>
</div>

<div id="main">
  %include
  <div class="clearer"></div>
</div>
