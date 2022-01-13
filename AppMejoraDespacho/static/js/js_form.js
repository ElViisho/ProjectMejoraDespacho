$(document).ready(function() {
    $('#nvv_selector').select2();
});

$('#nvv_selector').change(function() {
    var nvv = $(this).val();

    $.ajax({
        success: function () {
            $('#id_nvv').val(nvv);
        }
    })
})

var phoneInputField = document.querySelector("#phone");
var phoneInput = window.intlTelInput(phoneInputField, {
    initialCountry: "cl",
    preferredCountries: ["cl", "ar", "pe", "bo"],
    utilsScript:
       "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
    autoPlaceholder: "off",
    separateDialCode: "true"
});


$('#phone').change(function() {
    var phoneNumber = phoneInput.getNumber();

    $.ajax({
        success: function() {
            $('#id_cont_telefono').val(phoneNumber);
        }
    })
})

$("#phone").keyup(function () {
    var phoneNumber = phoneInput.getNumber(intlTelInputUtils.numberFormat.E164);

    $.ajax({
        success: function () {
            $('#id_cont_telefono').val(phoneNumber);
        }
    })
})

window.onload = function () {
    var phone  = $("#id_cont_telefono").val();
    $("#phone").val(phone);
    
}





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