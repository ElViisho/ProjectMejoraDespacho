// Get cookies for form submition
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

// Array with the name of months for display
const nombresMeses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

// Display order of objects of table. It checks for permissions to know if it is downloadble to excel or not
function domDataTable() {
    if (permissions=='Despacho') return '<"top"iflp<"clear">>rtB<"bottom"iflp<"clear">>'
    return '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>'
}

// Initialize variable as nothing
let nvv = "";
let table = "";

$(document).ready(function() { 
    // Add plugin of DataTable to table of data
    table = $('#listado').DataTable({ 
        "dom": domDataTable(),    // Display order of objects of table
        "columns": [        // Define properties for the columns of the table 
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
            },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
        ],
        "search": {     // Searches for the whole match and not each word individually
            "smart": false
        },
        language: {     // In spanish
            url: 'https://cdn.datatables.net/plug-ins/1.11.3/i18n/es-cl.json'
        },
        // Scrolling options
        "scrollX": true,
        "scrollY": "70vh",
        "scrollCollapse": true,
        "lengthMenu": [5, 10, 25, 50],  // Different options for how many to display per page
        order: [ 2, 'asc' ],            // Default order by date
        scrollToTop: true,              // When changing page it goes back to top of table
        buttons: [                      // Export to Excel button
            {
                extend: 'excel',
                classname: 'excel',
                text: 'Exportar tabla a excel',
                filename: function() {
                    d = new Date()
                    return "Ordenes de despacho " + d.getDate() + "-" + (nombresMeses[d.getMonth()]) + "-" + d.getFullYear() + " " + d.getHours() + "." + d.getMinutes();
                },
                exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13]
                },
                title: "Ordenes de despacho",
                customize: function(xlsx) {
                    var passedHeader = false;
                    if (passedHeader){
                        var styleSheet = xlsx.xl['styles.xml'];
                        var lastXfIndex = $('cellXfs xf', styleSheet).length - 1;
                        var n1 = '<numFmt formatCode="$ #,##0" numFmtId="300"/>';
                        var s1 = '<xf numFmtId="300" fontId="0" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1" xfId="0" applyNumberFormat="1"/>';
                        styleSheet.childNodes[0].childNodes[0].innerHTML += n1;
                        styleSheet.childNodes[0].childNodes[5].innerHTML += s1;

                        var fourDecPlaces = lastXfIndex + 1;

                        var sheet = xlsx.xl.worksheets['sheet1.xml'];
                        $('row c[r^="L"]', sheet).attr( 's', fourDecPlaces );
                    }
                    else {
                        passedHeader = true;
                    } 
                }
            }
        ]
    });    

    // When + symbol or NVV value is clicked, it shows all the relevant info
    $('#listado tbody').on('click', 'td.show_hide', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var data = row.data()[11].split("\\,\\,")
        data.push(row.data()[13])
        data.push(row.data()[14])
        data.unshift(row.data()[1])
 
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
    });
    
});

function textAreaChange() {
    var url = window.location.href;
    var textArea = document.getElementsByClassName('observaciones')[0];
    var nvv = textArea.id;
    var observaciones = textArea.value;
    
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        success: function () {
            // Post to change the observations of the order
            $.post(url, {"type": "observaciones", "nvv": nvv, "observacion": observaciones,})
            table.cell('#observacion' + nvv).data(observaciones)
        }
    })
}

// Initialize variable as 0 (falsey)
var listo = 0;

// For showing the child data
function format (d) {
    var n_guia = '';
    // Choses which button to show depending on if order is ready or not, and also if it must show the guide number or not
    listo = d[9];
    rowspan = 2;
    if (d[10] == 1) {
        n_guia = '<tr class="child_table">'+
            '<td>Número de guía:</td>'+
            '<td>' + d[6] + '</td>' +
        '</tr>'
        rowspan = 3;
    }
    
    // Child table for extra data
    return '<td class="child_table">' + 
        '<table cellpadding="5" cellspacing="0" border="0">'+
            '<tr class="child_table">' +
                '<td>Solicitado por:</td>' +
                '<td>' + d[8] + '</td>' +
                '<td>Valor neto:</td>' +
                '<td>$' + Number(d[11]).toLocaleString() + '</td>' +
            '</tr>' +
            '<tr class="child_table">' +
                '<td>Nombre vendedor:</td>' +
                '<td>' + d[7] + '</td>' +
                '<td>Condición de pago:</td>'+
                '<td>' + d[4] + '</td>'+
            '</tr>' +
            '<tr class="child_table">'+
                '<td>Fecha emisión NVV:</td>'+
                '<td>'+d[1]+'</td>'+
                '<td>Comprobante de pago:</td>' +
                '<td>' + d[5] + '</td>' +
            '</tr>'+
            '<tr class="child_table">'+
                '<td>Cliente:</td>'+
                '<td>'+d[2]+'</td>'+
                '<td rowspan="' + (rowspan+3) + '" style="vertical-align: top;">Obervaciones del pedido:</td>'+
                '<td rowspan="' + (rowspan+3) + '" style="vertical-align: top;">' + d[10] + '</td>'+
            '</tr>'+
            '<tr class="child_table">'+
                '<td>RUT Cliente:</td>'+
                '<td>' + d[3] + '</td>'+
            '</tr>'+
            '<tr class="child_table">' +
                '<td rowspan="' + rowspan + '" style="vertical-align: top;">Obervaciones solicitud:</td>'+
                '<td rowspan="' + rowspan + '" style="vertical-align: top;">' + '<textarea onchange="textAreaChange()" class="observaciones" id="'+ d[0] +
                '" style="resize:none" rows=2 cols=50 placeholder="Ingrese alguna observación en caso de ser pertinente">' + d[12] + '</textarea></td>'+
            '</tr>' +
            '<tr class="child_table"></tr>' +
            '<tr class="child_table"></tr>' +
            n_guia +
        '</table>'+
    '</td>';
}

// The prompt for confirmation of changes on table
function prompt_confirm(listo) {
    $('#confirm_texto').html(`¿Confirmas que quieres subir un nuevo comprobante de venta ${nvv}? (Borrará el antiguo en caso de existir)<br>`);
    $('#confirm_prompt_background').show();
    $('#confirm_prompt').show();
    $('#confirm_texto').show();
    $('#boton_confirm').show();
    $('#boton_cancel').show();
}

// To cancel the prompt
function cancelar() {
    $('#confirm_prompt_background').hide();
    $('#confirm_prompt').hide();
    $('#confirm_texto').hide();
    $('#boton_confirm').hide();
    $('#boton_cancel').hide();
}

// Confirm the prompt and send the post request to retrieve the guide number
function confirmar() {
    var url = window.location.href;

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        type: 'post',
        url: url,
        beforeSend: function () {
            // While waiting for response
            $('#confirm_texto').html('Cargando...');
            $('#boton_confirm').prop('disabled', true);
            $('#boton_cancel').prop('disabled', true);
        },
        data: {"type": "numero_guia", "nvv": nvv, "listo": listo},
        success: function () {
            // Reload table with new data
            window.location.reload();
        },
        error: function () {
            // Prompt the user there was no guide number and after 2 secondes reload table
            $('#confirm_texto').html('Error. Orden no tiene documento asociado. La página se recargará en breve.');
            setTimeout('window.location.reload()', 2000);
        },
        timeout: 5000 
    })

}