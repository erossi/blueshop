%
% rebase admin/admin_layout user=tpldata['user'], flash=tpldata['flash']
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Categorie</div>

    <div class="sideboxcontent" style="text-align: center;">
       <form action="items" method="post">
        <input type="hidden" name="whichform" value="chcat" />
        <select size="1" name="codcat" onchange="this.form.submit();">
% for cat in tpldata['cat']:
%   if cat[0] == tpldata['defcat']:
%     cat_id = cat[0]
%     cat_title = cat[2]
          <option value="{{cat[0]}}" selected="selected">{{cat[2]}}</option>
%   else:
          <option value="{{cat[0]}}">{{cat[2]}}</option>
%   end
% end
        </select><br />
        <br />
        <input type="submit" name="commit" value="Cambia"><br />
      </form>
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">File CSV</div>
    <div class="sideboxcontent">
      Carica il listino.csv per aggiornare le disponibilita'.<br />
      Alla fine del caricamento la pagina si aggiorna da sola. <br />
      Al momento ogni aggiornamento azzera prima tutte le disponibilita'
      a magazzino, ed elimina poi tutti gli articoli con disponibilita'
      0.<br />
      <br />
      <form action="upload_csv_pricelist" enctype="multipart/form-data" method="post">
        <input type="file" name="filedata" size="10" /><br />
        <input name="commit" type="submit" value="Carica" /><br />
      </form>
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Promo CSV</div>
    <div class="sideboxcontent">
      Carica il file promo.csv per attivare qualche promozione.<br />
      Il caricamento cancella tutte le promo eventualmente attive.<br />
      <br />
      <form action="upload_csv_promo" enctype="multipart/form-data" method="post">
        <input type="file" name="filedata" size="10" /><br />
        <input name="commit" type="submit" value="Carica" /><br />
      </form>
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Help</div>
    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margin-right: 1em;">
      Qui trovi il materiale che e' attualmente disponibile
      in magazzino.<br />
      <br />
      Puoi scegliere la categoria merceologica dal menu' a tendina qui' sopra,
      DEVI premere successivamente il pulsante 'vai'.<br />
      <br />
      Premendo <button>X</button>
      cancelli l'articolo dal database.<br />
      <br />
      Cliccando sulla descrizione dell'articolo puoi avere
      maggiori informazioni.<br />
    </div>
  </div>
</div>

<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">
      {{cat_title}}
    </div>

    <div class="contentboxcontent">
%
% for aid in tpldata['articles']:
%
% art = tpldata['articles'][aid]
%
<div id="item_{{aid}}" class="ItemRow">
  <table class="ItemRowTable">
    <tr>
      <td class="ItemRowIcon">
        <img alt="icon" src="/images{{art[13]}}" height="50" width="50" /> 
      </td>
      <td class="ItemRowDescription">
        <a href="/shop/show?aid={{aid}}">{{art[4]}}</a> ({{art[5]}})<br />
        <br />
        cod. <span class="ItemCode">{{art[3]}}</span>
        - Q.ta disponibile <span class="quantity">{{art[6]}}</span>
        <br />
        Stock: <span class="currency">&euro;&nbsp;{{art[8]}}</span>
        Vip: <span class="currency">&euro;&nbsp;{{art[9]}}</span>
        EU: <span class="currency">&euro;&nbsp;{{art[10]}}</span>
      </td>
      <td class="ItemRowCart">
        <form action="items" method="post">
          <input type="hidden" name="whichform" value="rmitem" />
          <input type="hidden" name="id" value="{{aid}}" />
          <input type="submit" name="commit" onclick="return confirm('Sei sicuro di voler rimuovere questo articolo?');" value="X" />
        </form>
      </td>
    </tr>
  </table>
</div>
%end
    </div>
  </div>
</div>
