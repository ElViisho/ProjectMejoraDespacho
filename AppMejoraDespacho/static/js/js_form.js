/*
Script where all the logic for the submit_nvv_form is
*/

// When document finished loading
$(document).ready(function() {
    // Make all elements that have different styling due to plugins,
    // ocupy 100% of the form width
    document.getElementById('id_nvv').style.width = "100%";
    document.getElementById('id_comuna').style.width = "100%";
    document.getElementById('id_region').style.width = "100%";
    document.getElementById('id_cont_telefono').style.width = "100%";
    // Make nvv, region and commune select2 (smart searchable selection)
    $('#id_nvv').select2();
    $('#id_region').select2();
    $('#id_comuna').select2();

    // Add listener to date picker to check if day selected is not weekend
    // and alert user if that's the case
    const picker = document.getElementById('id_fecha_despacho');
    const initialDate = picker.value;
    picker.addEventListener('change', function(e){
        var day = new Date(this.value).getUTCDay();
        if([6,0].includes(day)){
            e.preventDefault();
            this.value=initialDate;
            alert('fecha inválida');
        } 
    });

    change_dispath();
});


// Set the phone input field to use the plugin for country code and validation of valid phone number format
var phoneInputField = document.getElementById("id_cont_telefono");
var phoneInput = window.intlTelInput(phoneInputField, {
    initialCountry: "cl",
    preferredCountries: ["cl", "ar", "pe", "bo"],
    utilsScript:
       "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
    autoPlaceholder: "off",
    separateDialCode: "true"
});

// If the phone input changes, update the form field to for submition
$('#id_cont_telefono').change(function () {
    var phoneNumber = phoneInput.getNumber(intlTelInputUtils.numberFormat.E164);
    $("#id_cont_telefono").val(phoneNumber);
    $('#formulario').set('cont_telefono', phoneNumber);
})

// If file is uploaded, show its name
$("#id_comprobante_pago").change(function () {
    let file = $(this).val();
    let name = file.split("\\");
    let nombre = name[name.length-1];
    if (file != null) {
        $('#file_name').html(nombre);
        document.getElementById('id_comprobante_pago').nextSibling.nodeValue = ""; // If there was a cached value, delete it
    }
})

function change_dispath() {
    let val = document.querySelector('input[name="tipo_despacho"]:checked').value;
    
    if (val==1){
        $('#id_despacho_externo').show();
        $('#region_div').show();
        $('#id_region').prop('required', true);
        change_comunas(true);
    }
    else {
        $('#id_despacho_externo').hide();
        $('#region_div').hide();
        $('#id_region').prop('required', false);
        change_comunas(false);
    }
}

$('#id_tipo_despacho').change(change_dispath)

function change_comunas(cambiar) {
    var url = "ajax/load-comunas/";
    if (cambiar) var regionId = $('#id_region').val();
    else var regionId = 0;

    $.ajax({
        url: url,
        data: {
            'region': regionId
        },
        success: function (data) {
            $("#id_comuna").html(data);
        }
    });
}


// When value of region changes, change the available communes
$("#id_region").change(change_comunas)