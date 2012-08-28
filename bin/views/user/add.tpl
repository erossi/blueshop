%rebase layout.tpl error=tpldata['error'], notice=tpldata['notice']

<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle"><span>help</span></div>

    <div class="sideboxcontent">
      Per registrarsi inserite i
      Vostri dati anagrafici nei campi
      sottostanti.<br />
      <br />
      La registrazione non &egrave; automatica:
      la Vostra richiesta
      verr&agrave; vagliata da un nostro incaricato che Vi risponder&agrave;
      all'indirizzo e-mail da Voi indicato.<br />
      <br />
      <strong>NOTA: tutti i campi devono essere composti SOLO da lettere
      o numeri, altri caratteri non sono accettati.</strong>
    </div>
  </div>
</div>

<div id="content">
  <form action="/user/add" method="post">
  <div class="contentbox">
    <div class="contentboxtitle">Informazioni obbligatorie</div>
    <div class="contentboxcontent">
      <p>
        Ragione sociale / Nome e Cognome:
        <input name="ragsoc" size="50" type="text" value="{{tpldata['ragsoc']}}" />
      </p>
      <p>
        Partita IVA / Codice Fiscale:
        <input name="piva" size="15" type="text" value="{{tpldata['piva']}}" />
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
        <input name="password" size="20" type="password" value="" />
        Conferma Password:
        <input name="password_confirmation" size="20" type="password" />
      </p>
    </div>
  </div>

  <div class="contentbox">
    <div class="contentboxtitle">Indirizzo</div>
    <div class="contentboxcontent">
      <p> Indirizzo:
        <input name="sede_via" size="50" type="text" value="{{tpldata['sede_via']}}" />
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
      <p> Indirizzo:
        <input name="sede_via_2" size="50" type="text" value="{{tpldata['sede_via_2']}}" />
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

      <input type="submit" value="Invia la registrazione" />
    </div>
  </div>
  </form>

</div>
