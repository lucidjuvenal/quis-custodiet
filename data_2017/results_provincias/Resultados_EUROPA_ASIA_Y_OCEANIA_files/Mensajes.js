function ShowMessageAceptar() {
    $("#dialog").dialog({
        resizable: false,
        width: 350,
        height: "auto",
        modal: true,
        buttons: {
            Aceptar: function () {
                $(this).dialog("close");
            }
        }
    });
    return false;
};

