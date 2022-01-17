$(document).ready(function() {
    document.getElementById('id_nvv').style.width = "100%";
    document.getElementById('id_region').style.width = "100%";
    document.getElementById('id_comuna').style.width = "100%";
    document.getElementById('id_cont_telefono').style.width = "100%";
    $('#id_nvv').select2();
    $('#id_region').select2();
    $('#id_comuna').select2();


    const picker = document.getElementById('id_fecha_despacho');
    const initialDate = picker.value;
    var timeout = null;
    picker.addEventListener('keyup', function(e){
        var that = this;
        if (timeout !== null) {
            clearTimeout(timeout)
        }
        timeout = setTimeout(function() {
            var day = new Date(that.value).getUTCDay();
            if([6,0].includes(day)){
                e.preventDefault();
                that.value=initialDate;
                alert('fecha inválida');
            }
        }, 1000)
        
    });
});



var phoneInputField = document.getElementById("id_cont_telefono");
var phoneInput = window.intlTelInput(phoneInputField, {
    initialCountry: "cl",
    preferredCountries: ["cl", "ar", "pe", "bo"],
    utilsScript:
       "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
    autoPlaceholder: "off",
    separateDialCode: "true"
});

$('#id_cont_telefono').change(function () {
    var phoneNumber = phoneInput.getNumber(intlTelInputUtils.numberFormat.E164);
    $("#id_cont_telefono").val(phoneNumber);
    $('#formulario').set('cont_telefono', phoneNumber);
})


$("#id_comprobante_pago").change(function () {
    let file = $(this).val()
    let name = file.split("\\")
    let nombre = name[name.length-1]
    if (file != null) {
        $('#file_name').html(nombre)
    }
})

$("#id_region").change(function () {
    var url = "ajax/load-comunas/";
    var regionId = $(this).val();

    $.ajax({
        url: url,
        data: {
            'region': regionId
        },
        success: function (data) {
            $("#id_comuna").html(data);
        }
    });
});
if ($("#id_region").val() != 7) {
    var url = "ajax/load-comunas/";
    var regionId = $("#id_region").val();
    var comuna_actual = $("#id_comuna").val();
    $.ajax({
        url: url,
        data: {
            'region': regionId
        },
        success: function (data) {
            $("#id_comuna").html(data),
            $("#id_comuna").val(comuna_actual);
        }
    });
};