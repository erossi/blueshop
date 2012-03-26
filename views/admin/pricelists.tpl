%
% rebase admin/admin_layout user=user, flash=flash
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Files XLS</div>

    <div class="sideboxcontent">
      <a href="download_pricelist?pl=1">{{pricelists['filename1']}}</a> <br />
      {{pricelists['mtime_pl1']}} <br />
      <br />
      <a href="download_pricelist?pl=2">{{pricelists['filename2']}}</a> <br />
      {{pricelists['mtime_pl2']}} <br />
      <br />
      <a href="download_pricelist?pl=3">{{pricelists['filename3']}}</a> <br />
      {{pricelists['mtime_pl3']}} <br />
      <br />
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Load File</div>

    <div class="sideboxcontent">
      <form action="upload_pricelist" enctype="multipart/form-data" method="post">
        <input type="file" name="filedata" size="10" /><br />
        <input name="commit" type="submit" value="Carica" /><br />
      </form>
      <br />
      nb: Puoi caricare solo i file<br />
      stock.xls, vip.xls, eu.xls<br />
    </div>
  </div>

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
      Spedizione dei lisitini
    </div>

    <div class="contentboxcontent">
      <form action="pricelists" method="post">
        Soggetto :
        <input name="subject" size="50" type="text" value="{{pricelists['email_subject']}}" />
        <br /><br />
        Testo:<br />
        <textarea name="message" rows="15" cols="60">
          {{pricelists['email_text']}}
        </textarea>
        <br /><br />
        <input type="submit" value="Invia i listini" onclick="return confirm('Sei sicuro di voler procedere con la spedizione?');" />
     </form>
    </div>
  </div>
</div>
