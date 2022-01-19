function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

$('.Estado').change(function () {
    var url = window.location.href;
    var option = $(this).val();
    var nvv = this.id;

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        success: function () {
            $.post(url, {"type": "estado", "nvv": nvv, "option": option,});
        }
    })
})

let nvv = "";

$(document).ready(function() { 
    var table = $('#listado').DataTable({  
        "columns": [
            { "searchable": false, orderable: false },
            null,
            null,
            null,
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            null,
            null,
            { "searchable": false, orderable: false },
        ],    
        "search": {
            "smart": false
        },
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.11.3/i18n/es-cl.json'
        },
        "scrollX": true,
        "scrollY": "70vh",
        "scrollCollapse": true,
        order: [ 2, 'asc' ],
    });    

    $('#listado tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var data = row.data()[11].split("\\,")
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row and close others
            if ( table.row( '.shown' ).length ) {
                $('.dt-control', table.row( '.shown' ).node()).click();
            }
            nvv = row.data()[1];
            row.child( format(data) ).show();
            tr.addClass('shown');

            $('#numero_guia').change(function () {
                if ($(this).val() == "") {
                    $('#boton').prop('disabled', true);
                }
                else {
                    $('#boton').prop('disabled', false);
                }
            })
        }
    } );
});

var listo = 0;

function format (d) {
    listo = d[9];
    if (d[9] == 1) boton_guia_despacho = "Borrar número de guía";
    else boton_guia_despacho = "Marcar como despachado";

    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>' +
            '<td>Nombre vendedor:</td>' +
            '<td>' + d[7] + '</td>' +
        '</tr>' +
        '<tr>' +
            '<td>Solicitado por:</td>' +
            '<td>' + d[8] + '</td>' +
        '</tr>' +
        '<tr>'+
            '<td>Fecha emisión NVV:</td>'+
            '<td>'+d[0]+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Cliente:</td>'+
            '<td>'+d[1]+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>RUT Cliente:</td>'+
            '<td>' + d[2] + '</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Condición de pago:</td>'+
            '<td>' + d[3] + '</td>'+
        '</tr>'+
        '<tr>' +
            '<td>Comprobante de pago:</td>' +
            '<td>' + d[4] + '</td>' +
        '</tr>' +
        '<tr>'+
            '<td>Obervaciones:</td>'+
            '<td>' + d[5] + '</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Número de guía:</td>'+
            '<td>' + d[6] + '</td>' +
        '</tr>'+
        '<tr>'+
        `<td><input class="btn btn-default boton-sumbit" onclick="prompt_confirm(${listo})" id="boton" value="${boton_guia_despacho}" readonly></td>` +
            '<td></td>' +
        '</tr>'+
    '</table>';
}

function prompt_confirm(listo) {
    if (listo) {
        $('#confirm_texto').html(`¿Confirmas que quieres borrar la guía de despacho de la orden ${nvv}? (Dejará de estar marcada como despachada)<br>`);
    }
    else {
        $('#confirm_texto').html(`¿Confirmas que quieres marcar la orden ${nvv} como despachada? (Esto la hará invisible en la tabla)<br>`);
    }
    $('#confirm_prompt_background').show();
    $('#confirm_prompt').show();
    $('#confirm_texto').show();
    $('#boton_confirm').show();
    $('#boton_cancel').show();
}

function cancelar() {
    $('#confirm_prompt_background').hide();
    $('#confirm_prompt').hide();
    $('#confirm_texto').hide();
    $('#boton_confirm').hide();
    $('#boton_cancel').hide();
}

function confirmar() {
    var url = window.location.href;

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        success: function () {
            $.post(url, {"type": "numero_guia", "nvv": nvv, "listo": listo}, window.location.reload());
        }
    })

}