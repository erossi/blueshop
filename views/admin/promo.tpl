%
% rebase admin/admin_layout user=user, flash=flash
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Help</div>
    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margin-right: 1em;">
      <br />
    </div>
  </div>
</div>

<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">
      Spedizione delle promo
    </div>

    <div class="contentboxcontent">
      <form action="promo" method="post">
        Soggetto :
        <input name="subject" size="50" type="text" value="{{promo['email_subject']}}" />
        <br /><br />
        Testo:<br />
        <textarea name="message" rows="15" cols="60">
          {{promo['email_text']}}
        </textarea>
        <br /><br />
        <input type="submit" value="Invia le promo" onclick="return confirm('Sei sicuro di voler procedere con la spedizione?');" />
     </form>
    </div>
  </div>
</div>
