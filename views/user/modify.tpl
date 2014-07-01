%
%rebase store/store_layout.tpl user=tpldata, flash=tpldata['flash']
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle"><span>Attenzione</span></div>

    <div class="sideboxcontent">
      Per poter modificare la Ragione sociale, il Nome e Cognome,
      la partita IVA oppure il Codice Fiscale, dovete contattarci
      via email o telefonicamente.<br />
      <br />
      <strong>NOTA: tutti i campi devono essere composti SOLO da lettere
      o numeri, altri caratteri non sono accettati.</strong>
    </div>
  </div>
</div>

<div id="content">
  <form action="/user/modify" method="post">
  <div class="contentbox">
    <div class="contentboxtitle">Informazioni obbligatorie</div>
    <div class="contentboxcontent">
      <p>
        Ragione sociale / Nome e Cognome:
        <strong>{{tpldata['ragsoc']}}</strong>
      </p>
      <p>
        Partita IVA / Codice Fiscale:
        <strong>{{tpldata['piva']}}</strong>
      </p>
      <p>
        <i>Indicate i dati della persona che contatteremo per
           indicare l'avvenuta registrazione.</i><br />
        Nome e Cognome del responsabile commerciale:
        <input name="respcom" size="50" type="text" value="{{tpldata['respcom']}}" />
      </p>
      <p>
        <i>Indicate l'indirizzo al quale manderemo conferma dell'avvenuta registrazione</i><br />
        E-Mail:
        <input name="email" size="50" type="text" value="{{tpldata['email']}}" />
      </p>
      <p>
        Vuoi ricevere il listino via email: &nbsp;
        <select name="email_listino">
% if tpldata['email_listino'] == 't':
          <option value="t" select="selected">Si</option>
% else:
          <option value="f" select="selected">No</option>
% end
          <option value="t">Si</option>
          <option value="f">No</option>
        </select>
      </p>
      <p>
        <i>La password deve essere da 6 a 10 caratteri e puo' essere composta da numeri e lettere, sia minscole che MAIUSCOLE.</i>
        <br />
        Password:
        <input name="password" size="20" type="password" value="{{tpldata['password']}}" />
        Conferma Password:
        <input name="password_confirmation" size="20" type="password" value="{{tpldata['password']}}" />
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
       la correttezza delle informazioni sopra indicate. La conferma vale anche come consenso implicito all'utilizzo dei dati personali
       ai sensi di legge.
       </p>

      <input type="submit" value="Modifica la registrazione" />
    </div>
  </div>
  </form>

  <div class="contentbox">
    <div class="contentboxtitle">Eliminazione Utente</div>
      <div class="contentboxcontent">
        <p>
         <strong>Attenzione:</strong>
L'eliminazione dal sito implica la rimozione di tutte
le informazioni relative all'utente dal nostro database web.
Queste
informazioni non potranno essere recuperate in un secondo
momento, sara' quindi necessario fare una nuova registrazione.
<br />
<br />
<strong>Nota:</strong> Questa cancellazione NON comporta
l'eliminazione delle informazioni Fiscali eventualmente
presenti nel sistema contabile, obbligatorie ai sensi di legge.
        </p>
        <div align="center">
          <br />
          <a href="rmuser">
          <button onclick="return confirm('Sei sicuro di volerTi Cancellare dal sito?');"> Cancella Utente </button>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
