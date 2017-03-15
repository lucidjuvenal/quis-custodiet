function pageLoad() {

    if (grecaptcha != null) {
        grecaptcha.render('captchaResultados', {
            'sitekey': '6LfsvhUUAAAAAGUUILj726oSefrhdeHFXdeQyAF4',
            'theme': 'clear'
        });
        grecaptcha.reset();
    }
}

(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date(); a = s.createElement(o),
    m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
})(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-91420599-1', 'auto');
ga('send', 'pageview');

function switchColors(element) {
    links = document.getElementsByTagName("li");
    for (var i = 0 ; i < links.length ; i++)
        links.item(i).style.color = '#424242';
    element.style.color = '#0059C6';
}

function GraficoBarra() {
    document.getElementById("trBarra").style.display = '';
    document.getElementById("trPie").style.display = 'none';
}
function GraficoPie() {
    document.getElementById("trBarra").style.display = 'none';
    document.getElementById("trPie").style.display = '';
}

function Esconder(id, eleme) {

    var x = document.getElementsByClassName("TotalRows");
    for (i = 0; i < x.length; i++) {
        if (document.getElementById(id) != x[i])
            x[i].style.display = 'none';
    }

    var y = document.getElementsByClassName("PartentRows");
    for (i = 0; i < y.length; i++) {
        if (eleme != y[i]) {
            y[i].style.fontWeight = 'normal';
            y[i].style.background = "#ffffff";
        }
    }


    var estado = document.getElementById(id).style.display;


    //alert(estado);
    if (estado == 'none') {
        document.getElementById(id).style.display = '';
        eleme.style.fontWeight = 'bold';
        eleme.style.background = "#81BEF7";
    }
    else {
        eleme.style.fontWeight = 'normal';
        document.getElementById(id).style.display = 'none';
        eleme.style.background = "#ffffff";
    }
}

function CallClick(nomRec, codigo) {
    PageMethods.CreateSessionViaJavascript(nomRec, codigo);
    document.getElementById('btnSelected').click();
}

function abrir(vrUrl) {
    // alert(vrUrl);
    $.colorbox({ href: vrUrl, iframe: true, width: "95%", height: "92%" });
    //$(".iframe").colorbox({ iframe: true, width: "90%", height: "90%" });
}


$(window).keypress(function (event) {
    var x = event.which || event.keyCode;
    var ctrlDown = event.altKey || event.metaKey;
    if (x == 123) {
        return false;
    }
});

$(document).on("contextmenu", function (e) {
    e.preventDefault();
});