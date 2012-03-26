%rebase layout.tpl flash=flash

<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle"><span>Attenzione</span></div>

    <div class="sideboxcontent">
      Per poter recuperare i dati di accesso in automatico, rispettando la
      attuale normativa relativa alla privacy,
      e' necessario che l'indirizzo email usato
      nella registrazione sia attivo.<br />
      <br />
      I dati di registrazione verranno spediti alla email registrata.<br />
      <br />
      Se avete cambiato indirizzo email
      <b>DOVETE OBBLIGATORIAMENTE</b> contattarci telefonicamente
      o per mail al fine di aggiornare Vs. dati.<br />
      <br />
      Per ulteriori informazioni chiamare lo
      051/405050 oppure scrivere una email a:<br />
      commerciale@bluetechinformatica.com<br />
    </div>
  </div>
</div>

<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">Recupero Password</div>
    <div class="contentboxcontent">
      <form action="/main/recover_password" method="post">
        <p>
          Partita IVA/Codice Fiscale inserito al momento della registrazione:<br />
	  <input name="piva" size="30" type="text" /><br />
        </p>
        <p>Oppure</p>
        <p>
          E-Mail:
	  <input name="email" size="50" type="text" /><br />
        </p>
        <input name="commit" type="submit" value="Invia la richiesta" />
      </form>
    </div>
  </div>
</div>
