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
            alert('Fecha inválida');
        } 
    });

    change_button();
    change_dispath();

    // Set the phone input field to use the plugin for country code and validation of valid phone number format
    let phoneInputField = document.getElementById("id_cont_telefono");
    let phoneInput = window.intlTelInput(phoneInputField, {
        initialCountry: "cl",
        preferredCountries: ["cl", "ar", "pe", "bo"],
        separateDialCode: true,
        formatOnDisplay: true,
        nationalMode: true,
    })

    function cambiarTelefono(){
        var dialCode = phoneInput.getSelectedCountryData()["dialCode"];
        var number = $("#id_cont_telefono").val();
        number = number.replace(/ /g,'')
        pattern = /^(\+(\d{1,3}))(\d{4,11})$/i
        if (pattern.test(number)){
            return;
        }
        pattern = /^(\d{4,11})$/i
        if (pattern.test(number)){
            $("#id_cont_telefono").val('+' + dialCode + number);
            return;
        }
        
    }
    phoneInputField.addEventListener('change', cambiarTelefono);
    phoneInputField.addEventListener('keyup', cambiarTelefono);

    cambiarTelefono();
});



window.onbeforeunload = function() {
    sessionStorage.setItem('comuna', $('#id_comuna').val());
}

$('#id_nvv').change(change_button);
$('#id_comuna').change(change_button)

function change_button() {
    let val_nvv = document.querySelector('#id_nvv').value;
    let val_comuna = document.querySelector('#id_comuna').value;

    if (val_nvv == 0 || val_comuna == 0){
        $('#boton').prop('disabled', true);
    }
    else {
        $('#boton').prop('disabled', false);
    }
}


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
    
    // Is external dispatch
    if (val==1){
        $('#id_despacho_externo').show();
        $('#id_direccion_despacho_externo').show();
        $('#id_despacho_externo').prop('required', true);
        $('#id_direccion_despacho_externo').prop('required', true);
        $('#region_div').show();
        $('#id_region').prop('required', true);
        change_comunas(true);
    }
    // Is dispatch with DIMACO
    else {
        $('#id_despacho_externo').hide();
        $('#id_direccion_despacho_externo').hide();
        $('#id_despacho_externo').prop('required', false);
        $('#id_direccion_despacho_externo').prop('required', false);
        if (sucursal != 1){
            $('#region_div').hide();
            $('#id_region').prop('required', false);
        }
        else $('#id_region').prop('required', true);
        change_comunas(false);
    }
}

$('#id_tipo_despacho').change(change_dispath)

function change_comunas(cambiar) {
    var url = "ajax/load-comunas/";
    if (cambiar) var regionId = $('#id_region').val();
    else var regionId = 0;

    var url_string = window.location.href
    var url_param = new URL(url_string);
    var sucursal = url_param.searchParams.get("sucursal");

    $.ajax({
        url: url,
        data: {
            'region': regionId,
            'sucursal': sucursal
        },
        success: function (data) {
            $("#id_comuna").html(data);
        }
    }).done(function() {
        // Restore value of comunne before reload
        var comuna = sessionStorage.getItem('comuna');
        if (comuna){
            $("#id_comuna").val(comuna);
        }
        sessionStorage.clear();

        if ($("#id_region").prop('required') && $('#id_region').val()==0){
            $("#id_comuna").val(0);
            $("#id_comuna").prop('disabled', true);
        }
        else {
            $("#id_comuna").prop('disabled', false);
        }

        change_button();
    });
}


// When value of region changes, change the available communes
$("#id_region").change(change_comunas)