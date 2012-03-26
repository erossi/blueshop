<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"/static/xhtml1-transitional.dtd">
<html xmlns="/static/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta http-equiv="Content-Language" content="en" />
  <link rel="shortcut icon" href="/images/favicon.ico" />
  <title>Blueshop</title>
  <link type="text/css" rel="stylesheet" media="screen" href="/static/stylesheets/style.css">
  <link type="text/css" rel="stylesheet" media="screen" href="/static/stylesheets/loginstyle.css">
</head>

<body>
<div id="main">

%if ('error' in vars()) and (error):
<div id="error">
  Error: {{error}}
</div>
%end

<div id="registrazione">
  <span style="font-size: 1.5em;">
    <a href="/user/add">Registrati</a>
  </span>
  <p>
    Se non avete ancora un Vostro Codice<br />
    Utente personale potete richiederlo<br />
    compilando un semplice modulo. La <br />
    vostra richiesta verr&agrave; vagliata <br />
    da un nostro responsabile che Vi<br />
    risponder&agrave; prontamente.<br />
  </p>
</div>

<div id="login">
  <span style="font-size: 1.5em; color: blue;">
    Login
  </span>
  <br /><br />

  <form action="/user/login" method="post">
    email:
    <input id="user_email" name="email" size="15" type="text" /><br />
    Password:
    <input id="user_password" name="password" size="15" type="password" /><br />
    <br />
    <input name="commit" type="submit" value="Entra" />
  </form>
</div>

<div id="recuperopassword">
  <span style="font-size: 1.5em;">
    <a href="/main/recover_password">Recupero password</a>
  </span>
  <p>
    Se avete dimenticato la<br />
    vostra username o la vostra<br />
    password, oppure in fase di<br />
    registrazione il server vi risponde<br />
    che la Vs. ditta e' gia' stata registrata.<br />
  </p>
</div>

<div id="chisiamo">
  <span style="font-size: 1.5em;">
    <a href="/main/contacts">Chi siamo</a>
  </span>
  <p>
    La Ns. ditta ha sede in<br />
    una moderna zona industriale di<br />
    Bologna, facilmente raggiungibile<br />
    dalle principali strade e autostrade,<br />
    nonche' dall'Aereoporto Guglielmo <br />
    Marconi.<br />
  </p>
</div>

</div>

%include footer_layout

</body>
</html>
