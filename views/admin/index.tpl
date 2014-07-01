%
%rebase admin/admin_layout user=tpldata['user'], flash=tpldata['flash']
%
<script type="text/javascript" src="/static/javascripts/store.js">
</script>

<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Categorie</div>

    <div class="sideboxcontent">
    Ci sono {{len(tpldata['cat'])}} categorie nel database.<br />
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Aggiungi</div>

    <div class="sideboxcontent" style="text-align: left;">
       <form action="/admin/index" method="post">
        Codice:
        <input type="text", name="catcode", size="5" /><br />
        Descrizione:
        <input type="text", name="description", size="10" /><br />
        <INPUT type="submit" name="commit" value="Aggiungi"><br />
      </form>

    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Help</div>
    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margin-right: 1em;">
      NON Cancellare la categoria<br />
      '0 - Offerte'<br />
      altrimenti s'inkioda tutto!!! <br />
      <br />
      Puoi aggiungere una categoria merceologica qui' sopra,
      DEVI premere successivamente il pulsante 'aggiungi'.<br />
      <br />
      Puoi modificare sia il codice, che la descrizione di una categoria
      direttamente e poi premi 'modifica'. <br />
      <br />
      Premendo <button>X</button>
      elimini la categoria.<br />
      <br />
    </div>
  </div>
</div>

<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">Title</div>
    <div class="contentboxcontent">
%
% for category in tpldata['cat']:
% img_name = '/categories/' + str(category[1]) + '.png'
%
      <div style="min-height: 80px;">
        <form action="/admin/index" method="post">
          <img alt="icon" src="/images{{img_name}}" height="50" width="50" /> 
          <input type="hidden" name="id" value="{{category[0]}}" />
          {{category[0]}}
          <input type="text" name="catcode" size="5" value="{{category[1]}}" />
          <input type="text" name="description" size="30" value="{{category[2]}}" />
          <input type="submit" name="commit" value="Modifica">
          <input type="submit" name="commit" onclick="return confirm('Sei sicuro di voler cancellare la categoria?');" value="X" />
        </form>
      </div>
%
% end
%
    </div>
  </div>
</div>
