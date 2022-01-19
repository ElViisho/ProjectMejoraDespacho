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

const nombresMeses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

let nvv = "";

$(document).ready(function() { 
    var table = $('#listado').DataTable({ 
        "dom": '<"top"iflp<"clear">>rtB<"bottom"iflp<"clear">>',
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
            { "searchable": false, orderable: false, render: function (data, type, row) {
                x = []
                for (i in data){
                    switch(data[i]){
                        case "0": x.push("En preparación"); break;
                        case "1": x.push("Preparado"); break;
                        case "2": x.push("Tubos"); break;
                        case "3": x.push("Cañería"); break;
                        case "4": x.push("Rollos"); break;
                        case "5": x.push("Despachado"); break;
                        default: x.push(""); break;
                    }
                }
                return x;
            }
            }
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
        "lengthMenu": [10, 25, 50],
        order: [ 2, 'asc' ],
        scrollToTop: true,
        buttons: [
            {
                extend: 'excel',
                classname: 'excel',
                text: 'Exportar tabla a excel',
                filename: function() {
                    d = new Date()
                    return "Ordenes de despacho " + d.getDate() + "-" + (nombresMeses[d.getMonth()]) + "-" + d.getFullYear();
                },
                exportOptions: {
                    columns: [ 1, 2, 3, 4, 5, 7, 9, 10, 12]
                },
                title: "Ordenes de despacho",
            }
        ]
    });    

    $('#listado tbody').on('click', 'td.show_hide', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var data = row.data()[11].split("\\,")
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Close others
            table.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
                if (this.child.isShown()) {
                  this.child.hide();
                  $(this.node()).removeClass('shown');
                }
            });
            // Open this row
            nvv = row.data()[1];
            row.child( format(data) ).show();
            tr.addClass('shown');
        }
    } );

    if (permisos == 'Despacho') {
        $('.Estado').on('change', function () {
            var url = window.location.href;
            var option = $(this).val();
            var nvv = this.id;

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

            $.ajax({
                success: function () {
                    $.post(url, {"type": "estado", "nvv": nvv, "option": option,}),
                    table.cell('#estado_string' + nvv).data(option)
                }
            })
        })
    }
});

var listo = 0;

function format (d) {
    listo = d[9];
    if (d[9] == 1) boton_guia_despacho = "Borrar número de guía";
    else boton_guia_despacho = "Marcar como despachado";

    var boton_despacho = '';
    if (permisos == 'Despacho') {
    boton_despacho = '<tr>'+
    `<td colspan='2' style='text-align: center'><input class="btn btn-default boton-sumbit" onclick="prompt_confirm(${listo})" id="boton" value="${boton_guia_despacho}" readonly></td>` +
    '</tr>';}   

    return '<table class="child_table" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
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
        boton_despacho +
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