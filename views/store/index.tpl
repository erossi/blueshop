%
% rebase store/store_layout user=tpldata['user'], flash=tpldata['flash']
%
<script type="text/javascript" src="/static/javascripts/store.js">
</script>

<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Categorie</div>
    <div class="sideboxcontent" style="text-align: center;">
       <form action="index" method="post">
        <select size="1" name="codcat" onchange="this.form.submit();">
% for cat in tpldata['cat']:
%  if cat[0] == tpldata['defcat']:
%   cat_id = cat[0]
%   cat_title = cat[2]
          <option value="{{cat[0]}}" selected="selected">{{cat[2]}}</option>
%  else:
          <option value="{{cat[0]}}">{{cat[2]}}</option>
%  end
% end
        </select><br />
        <br />
        <INPUT type="submit" value="Vai"><br />
      </form>
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Help</div>
    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margin-right: 1em;">
      Qui trovi il materiale che e' attualmente disponibile
      in magazzino.<br />
      <br />
      Per il materiale ordinabile a listino, ma non presente in magazzino, dovete
      contattare il Vs. commerciale.<br />
      <br /> 
      Puoi scegliere la categoria merceologica dal menu' a tendina qui' sopra,
      DEVI premere successivamente il pulsante 'vai'.<br />
      <br />
      Premendo
      <img alt="icon" src="/images/carrello.png" /> 
      modifichi il tuo carrello ed aggiorni i totali.<br />
      <br />
      Premendo <button>X</button>
      azzeri la quantita' presente nel carrello.<br />
      <br />
      Cliccando sulla descrizione dell'articolo puoi avere
      maggiori informazioni.<br />
      <br />
      Puoi andare in qualsiasi momento sul menu' "carrello" per consultare
      tutto il contenuto del tuo carrello ed eventualmente concludere
      l'ordine.<br />
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
% # tpldata['articles'] is {codid: ['id', '...', ...]}
% # art is (id, cat_id, u'catcode', u'artcode', u'artdesc', u'artdesc2',
% #     QTA, Price, price1, price2, price3, price4,
% #     'details info', 'image path',
% #     'promo boolean t or f', promo price , promo qta,
% #     'order_days', u'created_at', u'updated_at')
%
% art = tpldata['articles'][aid]
%
% # set the price list for this user.
% price = art[7 + tpldata['user']['listino']]
% strprice = '{:5.2f}'.format(price)
%
% if aid in tpldata['mychart']:
%     qta = tpldata['mychart'][aid]
%     total = price * qta
% else:
%     qta = 0
%     total = 0
% end
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
        Prezzo: <span class="currency">&euro;&nbsp;{{strprice}}</span>
        - Totale nel carrello:
        <span id="itemPrice_{{aid}}" class="currency"></span>
        <script type="text/javascript">
           prettyTotalPrice({{aid}}, {{price}}, {{qta}})
        </script>
      </td>
      <td class="ItemRowCart">
%#        <form method="get" onSubmit="ajSubmitNewQta({{aid}}, {{price}});" onChange="ajSubmitNewQta({{aid}}, {{price}});" >
        <form onSubmit="return (false);">
          <input type="text" id="itemQta_{{aid}}" name="qta" onChange="ajSubmitNewQta({{aid}}, {{price}});" size="3" value="{{qta}}" />
%#          <input type="submit" style="visibility:hidden" />
        </form>
      </td>
    </tr>
  </table>
</div>
%end
    </div>
  </div>
</div>
