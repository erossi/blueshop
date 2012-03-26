%
% rebase admin/admin_layout user=user, flash=flash
% prev = allusers['prev']
% next = allusers['next']
% first = allusers['first']
% last = allusers['last']
%
<div id="sidebar">
  <div class="sidebox">
    <div class="sideboxtitle">Utenti</div>

    <div class="sideboxcontent" style="text-align: left;">
      {{allusers['total']}} utenti nel database.<br />
      {{allusers['price1']}} a listino stock.<br />
      {{allusers['price2']}} a listino vip.<br />
      {{allusers['price3']}} a listino EU.<br />
      {{allusers['email']}} hanno email valida.<br />
      {{allusers['www']}} hanno accesso web.<br />
      {{allusers['promo']}} ricevono promo.<br />
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Search</div>

    <div class="sideboxcontent">
      Inserisci una o piu' parole, saranno ricercate nella
      ragione sociale e nell'indirizzo email.<br />
      <br />
      <form action="users" method="post">
% if search:
        <input name="cursor" type="hidden" value="{{cursor}}" />
        <input name="search" size="20" type="text" value="{{search}}" />
% else:
        <input name="search" size="20" type="text" />
% end
        <input name="commit" type="submit" value="Cerca" /><br />
      </form>
    </div>
  </div>

  <div class="sidebox">
    <div class="sideboxtitle">Help</div>
    <div class="sideboxcontent" style="text-align: left; margin-left: 1em; margin-right: 1em;">
      Qui trovi l'elenco utenti.<br />
      <br />
      Tipicamente un nuovo cliente e' nella condizione:<br />
      @OK - true<br />
      @Lst - non importa <br />
      @Promo - non importa <br />
      www - false<br />
      Lst - 4<br />
      <br />
      @OK: L'email dell'utente e' un mail valido. Solo l'amministratore
      puo' cambiare questo parametro.<br />
      Puo' indicare una nuova registrazione o una mail sbagliata, ma
      lascia la possibilita' di accesso web. Ovviamente i due parametri
      @Lst e @Promo non contano se questo e' disattivato.<br />
      <br />
      @Lst: Il cliente vuole il listino via email, questo parametro e'
      a discrezione del cliente e non dovrebbe essere modificato
      dall'amministratore.<br />
      <br />
      @Promo: Come per @Lst, solo relativo alle promo.<br />
      <br />
      www: Accesso al web. Solo l'amministratore puo' cambiare questo
      parametro.<br />
      Tipicamente e' disattivato sulle nuove registrazioni, non 
      ancora abilitate.<br />
      <br />

      Cliccando sulla descrizione dell'articolo puoi avere
      maggiori informazioni.<br />
    </div>
  </div>
</div>

<div id="content">
  <div class="contentbox">
    <div class="contentboxtitle">
      Clienti [{{first}} - {{last}}]
    </div>

    <div class="contentboxcontent">
%
% if len(allusers['list']):
      <table>
        <tr>
          <th style="width: 8em; text-align: left;">P.IVA</th>
          <th style="width: 10em; text-align: left;">Ragione Sociale</th>
          <th style="width: 10em; text-align: left;">email</th>
          <th> @OK </th>
          <th> @Lst </th>
          <th> @Prm </th>
          <th> www </th>
          <th> Lst </th>
        </tr>
%
% for thisuser in allusers['list']:
        <tr>
          <th style="width: 8em; text-align: left;">
            {{thisuser[1]}}
          </th>
          <th style="width: 10em; text-align: left;">
            <a href="/admin/changeuser?id={{thisuser[0]}}">
            {{thisuser[2]}}
            </a>
          </th>
          <th style="width: 10em; text-align: left;">
            {{thisuser[3]}}
          </th>
% if thisuser[4] == 'f':
          <th style="background-color: red;">
% else:
          <th>
% end
            {{thisuser[4]}}
          </th>
% if thisuser[5] == 'f':
          <th style="background-color: red;">
% else:
          <th>
% end
            {{thisuser[5]}}
          </th>
% if thisuser[6] == 'f':
          <th style="background-color: red;">
% else:
          <th>
% end
            {{thisuser[6]}}
          </th>
% if thisuser[7] == 'f':
          <th style="background-color: red;">
% else:
          <th>
% end
            {{thisuser[7]}}
          </th>
% if thisuser[8] == 'f':
          <th style="background-color: red;">
% else:
          <th>
% end
            {{thisuser[8]}}
          </th>
        </tr>
% end
%
      </table>
      <br />
      <form action="/admin/users" method="post">
        <input name="search" type="hidden" value="{{search}}" />
        <input name="cursor" type="hidden" value="{{cursor}}" />
% if prev or cursor:
        <input name="cursorprev" type="hidden" value="{{prev}}" />
        <input name="commit" type="submit" value="<< prev" />
% else:
        prev
% end
%
% if next:
        <input name="cursornext" type="hidden" value="{{next}}" />
        <input name="commit" type="submit" value="next >>" />
% else:
        next
% end
      </form>
%
% else:
%
      <p>Non ci sono clienti registrati.</p>
% end
%
    </div>
  </div>
</div>
