/*var prevNowPlaying = null;

function pageLoad() {
    var timeOut = $("input:hidden[id*='hfTimeOut']").val();
    //alert(timeOut);
    if (prevNowPlaying) {
        clearInterval(prevNowPlaying);
    }
    prevNowPlaying = window.setInterval("TimeextendOrExpired()", ((timeOut) * 60 * 1000) - 60000); // 60000 milisegundos antes cierra sesión 
    //prevNowPlaying = window.setInterval("TimeextendOrExpired()", ((1) * 60 * 1000) - 55000);
}
function TimeextendOrExpired() {
    document.getElementById('Salir').click();
    console.log('La sesión se ha cerrado por inactividad!');
}*/

$(document).ready(function () {

    $('.ir-arriba').click(function () {
        $('body, html').animate({
            scrollTop: '0px'
        }, 300);
    });

    $(window).scroll(function () {
        if ($(this).scrollTop() > 0) {
            $('.ir-arriba').slideDown(300);
        } else {
            $('.ir-arriba').slideUp(300);
        };
    });

});


//DESHABILITA LA OPCIÓN DE ATRÁS
function DisableBackButton() {
    window.history.forward()
}
DisableBackButton();
window.onload = DisableBackButton;
window.onpageshow = function (evt) { if (evt.persisted) DisableBackButton() }
window.onunload = function () { void (0) }