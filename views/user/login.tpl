%rebase layout.tpl error=error, notice=None
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle"><span>Login</span></div>

    <div class="sideboxcontent">
      <form action="/user/login" method="post">
        email:
        <input id="user_email" name="email" size="14" type="text" />
        <br />
        Password:
        <input id="user_password" name="password" size="10" type="password" />
        <br /><br />
	<input name="commit" type="submit" value="Login" />
       </form>
    </div>
  </div>
</div>

<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">Info</div>
    <div class="contentboxcontent">

In this area you should put the infos relative
to your company or this web site in general.<br />
<br />

For example you can put a link to the
<a href="/user/add">add_users page</a>,
which can be usefull if you want to let users to
register.<br />
<br />

Or a link to
<a href="/main/recover_password">recover password page</a>.<br />
<br />

Another cool page is the
<a href="/main/contacts">who we are page.</a><br />
<br />

Last, but no least (and not implemented yet!) is the about page,
showing infos about this software and licences.<br />

    </div>
  </div>
</div>
