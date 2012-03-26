% thisuser = tpldata['user']
% thisgrandtotal = 0
%
Salve {{thisuser['ragsoc']}}

ti confermiamo l'inserimento del seguente ordine:

Nome: {{thisuser['ragsoc']}}
P.IVA: {{thisuser['piva']}}
Att.ne: {{thisuser['respcom']}}

Sede Principale
  Indirizzo: {{thisuser['sede_via']}}, {{thisuser['sede_civico']}}
  CAP: {{thisuser['sede_cap']}} {{thisuser['sede_citta']}} ({{thisuser['sede_prov']}})
  {{thisuser['sede_stato']}}
  Tel: {{thisuser['sede_tel']}} - Fax: {{thisuser['sede_fax']}}

Sede secondaria
  Indirizzo: {{thisuser['sede_via_2']}}, {{thisuser['sede_civico_2']}}
  CAP: {{thisuser['sede_cap_2']}} {{thisuser['sede_citta_2']}} ({{thisuser['sede_prov_2']}})
  {{thisuser['sede_stato_2']}}
  Tel: {{thisuser['sede_tel_2']}} - Fax: {{thisuser['sede_fax_2']}}

Informazioni Aggiuntive all'ordine:

  {{thisuser['orderinfo']}}


Carrello:

% if len(tpldata['items']):
% for thisid in tpldata['items']:
% thisitem = tpldata['items'][thisid]
% thisqta = tpldata['mycart'][thisid]
% thistotalprice = thisitem['price'] * thisqta
% thisgrandtotal += thistotalprice
% # string-ify this value
% thisprice = '{:5.2f}'.format(thisitem['price'])
% thistotalprice = '{:5.2f}'.format(thistotalprice)

% if thisitem['desc2']:
{{thisqta}} {{thisitem['desc']}}, {{thisitem['desc2']}}
% else:
{{thisqta}} {{thisitem['desc']}}
% end
  {{thisitem['itemcode']}} cad.: {{thisprice}} tot: {{thistotalprice}} euro
% end # for thisitem
% else:
  Non ci sono articoli presenti nel carrello.
% end # if - else

Totale Ordine: {{thisgrandtotal}} + I.V.A.

La procedura d'ordine NON e' automatica, questa e' la copia del tuo ordine inserito via Web.
Eventuali promozioni, sconti, o variazioni all'ordine stesso saranno applicate prima della spedizione del materiale dai nostri responsabili.
In caso di pagamento anticipato dovete attendere, come di consueto, la proforma email o fax dell'ordine stesso.

Per qualsiasi problema potete contattarci via telefono o email.
Buona giornata

Blue Tech s.r.l.
