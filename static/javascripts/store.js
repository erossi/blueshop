function ajaxRequest()
{
    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        return new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        return new ActiveXObject("Microsoft.XMLHTTP");
    }
}

function ajSubmitNewQta(art_id, price)
{
    var xmlhttp = ajaxRequest();
    var qta = Number(document.getElementById("itemQta_" + art_id).value) || 0;
    var params = "aid=" + art_id + "&qta=" + qta;

    xmlhttp.open("GET", "/shop/buy?" + params, true);
    xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xmlhttp.send(null);

    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText == 'OK') {
                prettyTotalPrice(art_id, price, qta)
            } else {
                alert('returned qta: ' + newqta);
            }
        }
    }
}

// Substitute the content of span id=aid_totalprice with
// price * qta in the form of #.##
function prettyTotalPrice(aid, price, qta)
{
    var totalprice;

    totalprice = (price * qta).toFixed(2);
    document.getElementById("itemPrice_" + aid).innerHTML = "&euro; " + totalprice;
}

// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
