%rebase store/store_layout user=tpldata['user'], flash=tpldata['flash']

<script type="text/javascript" src="/static/javascripts/store.js">
</script>

<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Categorie</div>

    <div class="sideboxcontent" style="text-align: center;">
       <form action="index" method="post">
        <select size="1" name="codcat" onchange="this.form.submit();">

%for cat in tpldata['cat']:
	%if cat[0] == tpldata['defcat']:
          <option value="{{cat[0]}}" selected="selected">{{cat[2]}}</option>
	%else:
          <option value="{{cat[0]}}">{{cat[2]}}</option>
	%end
%end
        </select><br />
        <br />
        <INPUT type="submit" value="Vai"><br />
      </form>

    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Help</div>

    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margi
n-right: 1em;">
      Qui trovi il dettaglio dell'articolo selezionato.<br />
      <br />
      Quest'area e' ancora in fase di sviluppo al momento.
      Ce ne scusiamo.<br />
      <br />
      Puoi scegliere un'altra categoria merceologica dal menu' a
      tendina qui' sopra,
      DEVI premere successivamente il pulsante 'vai'.<br />
      nb: Questo ti riportera' alla lista di tutti gli articoli di quella
      categoria.<br />
      <br />
      Premendo
      <img alt="icon" src="/images/carrello.png" /> 
      modifichi il tuo carrello ed aggiorni i totali.<br />
      <br />
      Puoi andare in qualsiasi momento sul menu' "carrello" per consultare
      tutto il contenuto del tuo carrello ed eventualmente concludere
      l'ordine.<br />
    </div>

  </div>
</div>
%
% art = tpldata['item']
% aid = art[0]
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
<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">{{art[4]}}</div>

    <div class="contentboxcontent">

      <div id="article">
        <div id="article_logo">
          <img alt="icon" src="/images{{art[13]}}" height="150" width="150" /> 
        </div>

        <div>
          <p>{{art[5]}}</p>
          <p>Codice: <span class="ItemCode">{{art[3]}}</span> </p>
        </div>

        <div class="clearer"></div>
        
        <div style="margin-top: 2em; ">
          <p>Quantita' disponibile:
            <span class="quantity">{{art[6]}}</span>
          </p>
          <p>Prezzo:
            <span class="currency">&euro;&nbsp;{{strprice}}</span>
          </p>

        <form onSubmit="return (false);">
          <p> 
            In ordine nel carrello
          <input type="text" id="itemQta_{{aid}}" name="qta" onChange="ajSubmitNewQta({{aid}}, {{price}});" size="3" value="{{qta}}" />
          </p>
        </form>

        <p>Totale in ordine:
          <span id="itemPrice_{{aid}}" class="currency"></span>
          <script type="text/javascript">
             prettyTotalPrice({{aid}}, {{price}}, {{qta}})
          </script>
        </p>
        </div>

      </div>

    </div>
  </div>
</div>
