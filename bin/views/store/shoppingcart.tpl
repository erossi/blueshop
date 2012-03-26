% thisuser = tpldata['user']
% thisgrandtotal = 0
% rebase store/store_layout user=thisuser, flash=tpldata['flash']
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Attenzione</div>
    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margin-right: 1em;">
      Qui trovi il contenuto del tuo carrello con il totale di spesa.<br />
      <br />
      Prima di procedere e concludere l'ordine, ricorda:<br />
      <ul>
        <li>La procedura d'ordine NON e' automatica, copia del tuo ordine ti verra' spedito via email.</li>
        <li>Eventuali promozioni, sconti, o variazioni all'ordine stesso saranno applicate prima della spedizione del materiale dai nostri responsabili.</li>
        <li>In caso di pagamento anticipato dovete attendere, come di consueto, la proforma email o fax dell'ordine stesso.</li>
      </ul>
      Premendo <button>X</button>
      azzeri la quantita' presente nel carrello.<br />
    </div>
  </div>
</div>

<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">Carrello</div>

    <div class="contentboxcontent">
% if len(tpldata['items']):
      <table>
        <tr>
          <th>Descrizione</th>
          <th style="width: 100px">Cod.</th>
          <th style="width: 30px">Qta</th>
          <th style="width: 100px">Prezzo</th>
          <th style="width: 100px">Tot.</th>
          <th style="width: 30px">&nbsp;</th>
        </tr>
%
% for thisid in tpldata['items']:
% thisitem = tpldata['items'][thisid]
% thisqta = tpldata['mycart'][thisid]
% thistotalprice = thisitem['price'] * thisqta
% thisgrandtotal += thistotalprice
% # string-ify this value
% thisprice = '{:5.2f}'.format(thisitem['price'])
% thistotalprice = '{:5.2f}'.format(thistotalprice)
%
        <tr>
          <td>
            <a href="/shop/show?aid={{thisid}}">{{thisitem['desc']}}</a>
            <br />
% if thisitem['desc2']:
            {{thisitem['desc2']}}
% end
          </td>
          <td><span class="ItemCode">{{thisitem['itemcode']}}</span></td>
          <td><span class="quantity">{{thisqta}}</span></td>
          <td><span class="currency">&euro; {{thisprice}}</span></td>
          <td><span class="currency">&euro; {{thistotalprice}}</span></td>
          <td>
            <form action="cart" method="post">
              <input type="hidden" name="aid" value="{{thisid}}" />
              <input type="submit" name="commit" onclick="return confirm('Sei sicuro di voler rimuovere questo articolo?');" value="X" />
            </form>
          </td>
        </tr>
% end # for thisitem
      </table>
% else:
        <p>Non ci sono articoli presenti nel carrello.</p>
% end # if - else
    </div>
  </div>

  <div class="contentbox">
    <div class="contentboxtitle">Dati di spedizione</div>
    <div class="contentboxcontent">
      <p>
      Spett.le <strong>{{thisuser['ragsoc']}}</strong><br />
      &nbsp;- P.IVA: <strong>{{thisuser['piva']}}</strong><br />
      Att.ne: <strong>{{thisuser['respcom']}}</strong><br />
      </p>
      <table><tr>
      <td style="min-width: 20em;">
      <p><strong>Sede Principale</strong><br />
        Indirizzo: {{thisuser['sede_via']}}, {{thisuser['sede_civico']}}<br />
        CAP: {{thisuser['sede_cap']}} - {{thisuser['sede_citta']}}
        &nbsp;({{thisuser['sede_prov']}})<br />
        {{thisuser['sede_stato']}}<br />
        Tel: {{thisuser['sede_tel']}} - Fax: {{thisuser['sede_fax']}}<br />
      </p></td>
      <td>
      <p><strong>Sede secondaria</strong><br />
        Indirizzo: {{thisuser['sede_via_2']}}, {{thisuser['sede_civico_2']}}<br />
        CAP: {{thisuser['sede_cap_2']}} - {{thisuser['sede_citta_2']}}
        &nbsp;({{thisuser['sede_prov_2']}})<br />
        {{thisuser['sede_stato_2']}}<br />
        Tel: {{thisuser['sede_tel_2']}} - Fax: {{thisuser['sede_fax_2']}}<br />
      </p></td>
      </tr></table>
      <p>
        <strong> Potete scrivere eventuali variazioni nella spedizione nelle
        segnalazioni relative all'ordine qui' sotto.</strong>
      </p>
    </div>
  </div>

  <div class="contentbox">
    <div class="contentboxtitle">Conferma ordine</div>

    <div class="contentboxcontent">
      <span style="font-size: 1.5em;">Totale Ordine: 
      {{thisgrandtotal}}&nbsp;+ I.V.A.
      </span>
      <p>Informazioni aggiuntive o segnalazioni relative all'ordine</p>
      <form action="/shop/checkout" method="post">
        <textarea name="info" rows="5" cols="50"></textarea>
        <br /><br />
        <input type="submit" value="Concludi Ordine" />
      </form>
    </div>
  </div>
</div>
