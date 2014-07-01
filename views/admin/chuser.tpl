%
% rebase admin/admin_layout user=user, flash=flash
%
% listini = ('', 'stock', 'vip', 'EU', 'Nessuno')
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Help</div>
    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margin-right: 1em;">
      Tipicamente un nuovo cliente e' nella condizione:<br />
      Listino via mail - non importa<br />
      Promo via mail - non importa <br />
      Email valido - true<br />
      Accesso web - false<br />
      Listino - 4 o none<br />
      <br />
      NON Attivare l'accesso web ad un cliente che non abbia il
      listino 1 o 2, altrimenti al login crasha il sito.<br />
      <br />
      Non cancellare il tuo stesso utente da questo menu, se ti
      vuoi suicidare, fallo da un'altra parte, per esempio
      dalla modifica utente personale nello shop menu.
    </div>
  </div>
</div>

<div id="content">
  <form action="changeuser?id={{tpldata['id']}}" method="post">
    <input name="uid" type="hidden" value="{{tpldata['id']}}" />
  <div class="contentbox">
    <div class="contentboxtitle">Informazioni obbligatorie</div>
    <div class="contentboxcontent">
      <p>
        Ragione sociale / Nome e Cognome:
        <input name="ragsoc" size="50" type="text" value="{{tpldata['ragsoc']}}" />
      </p>
      <p>
        Partita IVA / Codice Fiscale:
        <input name="piva" size="30" type="text" value="{{tpldata['piva']}}" />
      </p>
      <p>
        Nome e Cognome del responsabile commerciale:
        <input name="respcom" size="50" type="text" value="{{tpldata['respcom']}}" />
      </p>
      <p>
        E-Mail:
        <input name="email" size="50" type="text" value="{{tpldata['email']}}" />
      </p>
      <p>
        listino via email: &nbsp;
        <select name="email_listino">
% if tpldata['email_listino'] == 't':
          <option value="t" select="selected">Si</option>
% else:
          <option value="f" select="selected">No</option>
% end
          <option value="t">Si</option>
          <option value="f">No</option>
        </select>
        &nbsp; promo via email: &nbsp;
        <select name="email_promo">
% if tpldata['email_promo'] == 't':
          <option value="t" select="selected">Si</option>
% else:
          <option value="f" select="selected">No</option>
% end
          <option value="t">Si</option>
          <option value="f">No</option>
        </select>
        &nbsp; Indirizzo email valido: &nbsp;
        <select name="email_valid">
% if tpldata['email_valid'] == 't':
          <option value="t" select="selected">Si</option>
% else:
          <option value="f" select="selected">No</option>
% end
          <option value="t">Si</option>
          <option value="f">No</option>
        </select>
      </p>
      <p>
        accesso web: &nbsp;
        <select name="web_access">
% if tpldata['web_access'] == 't':
          <option value="t" select="selected">Si</option>
% else:
          <option value="f" select="selected">No</option>
% end
          <option value="t">Si</option>
          <option value="f">No</option>
        </select>
        &nbsp; listino: &nbsp;
        <select name="listino">
          <option value="{{tpldata['listino']}}" select="selected">
            {{listini[tpldata['listino']]}}
          </option>
          <option value="1">Stock</option>
          <option value="2">Vip</option>
          <option value="3">EU</option>
          <option value="4">Nessuno</option>
        </select>
      </p>
      <p>
        <i>La password deve essere da 6 a 10 caratteri e puo' essere composta da numeri e lettere, sia minscole che MAIUSCOLE.</i>
        <br />
        Password:
        <input name="password" size="20" type="text" value="{{tpldata['password']}}" />
      </p>

      <p>
        <span>Registrato dal: {{tpldata['created_at']}}</span>
        &nbsp;
        <span>Utima modifica il: {{tpldata['updated_at']}}</span>
        <br />
% for i in range(len(tpldata['logins'])):
        <span>Login[{{i}}]: {{tpldata['logins'][i][0]}}</span><br />
% end
      </p>

    </div>
  </div>

  <div class="contentbox">
    <div class="contentboxtitle">Indirizzo</div>
    <div class="contentboxcontent">
      <p> Indirizzo e numero civico:

% if tpldata['sede_civico'] == '':
        <input name="sede_via" size="50" type="text" value="{{tpldata['sede_via']}}" />
% else:
        <input name="sede_via" size="50" type="text" value="{{tpldata['sede_via']}} {{tpldata['sede_civico']}}" />
% end

      </p>
      <p> CAP Citt&aacute; (Provincia):
        <input name="sede_cap" size="5" type="text" value="{{tpldata['sede_cap']}}" />
        <input name="sede_citta" size="30" type="text" value="{{tpldata['sede_citta']}}" />
        <input name="sede_prov" size="5" type="text" value="{{tpldata['sede_prov']}}" />
      </p>
      <p> Stato:
        <input name="sede_stato" size="50" type="text" value="{{tpldata['sede_stato']}}" value="Italia" />
      </p>
      <p> Telefono:
        <input name="sede_tel" size="30" type="text" value="{{tpldata['sede_tel']}}" />
        Fax:
        <input name="sede_fax" size="30" type="text" value="{{tpldata['sede_fax']}}" />
      </p>
    </div>
  </div>

  <div class="contentbox">
    <div class="contentboxtitle">Indirizzo sede operativa</div>
    <div class="contentboxcontent">
      <p> Indirizzo e numero civico:

% if tpldata['sede_civico_2'] == '':
        <input name="sede_via_2" size="50" type="text" value="{{tpldata['sede_via_2']}}" />
% else:
        <input name="sede_via_2" size="50" type="text" value="{{tpldata['sede_via_2']}} {{tpldata['sede_civico_2']}}" />
% end

      </p>
      <p> CAP Citt&aacute; (Provincia):
        <input name="sede_cap_2" size="5" type="text" value="{{tpldata['sede_cap_2']}}" />
        <input name="sede_citta_2" size="30" type="text" value="{{tpldata['sede_citta_2']}}" />
        <input name="sede_prov_2" size="5" type="text" value="{{tpldata['sede_prov_2']}}" />
      </p>
      <p> Stato:
        <input name="sede_stato_2" size="50" type="text" value="{{tpldata['sede_stato_2']}}" value="Italia" />
      </p>
      <p> Telefono:
        <input name="sede_tel_2" size="30" type="text" value="{{tpldata['sede_tel_2']}}" />
        Fax:
        <input name="sede_fax_2" size="30" type="text" value="{{tpldata['sede_fax_2']}}" />
      </p>
    </div>
  </div>

  <div class="contentbox">
    <div class="contentboxtitle">Attivita' svolta</div>
    <div class="contentboxcontent">
      <textarea name="attivita" rows="5" cols="50">{{tpldata['attivita']}}</textarea>
      <br />
      <p>
       <strong>Attenzione:</strong>
       Facendo clic sul pulsante "Conferma registrazione" si garantisce
       la correttezza delle informazioni sopra indicate.
       La conferma vale anche come consenso implicito all'utilizzo dei dati personali
       ai sensi di legge.
       </p>

      <input type="submit" value="Modifica la registrazione" />
    </div>
  </div>
  </form>

  <div class="contentbox">
    <div class="contentboxtitle">Eliminazione Utente</div>
      <div class="contentboxcontent">
        <div align="center">
          <a href="rmuser?id={{tpldata['id']}}">
          <button onclick="return confirm('Sei sicuro di voler rimuovere questo utente?');"> Cancella Utente </button>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
