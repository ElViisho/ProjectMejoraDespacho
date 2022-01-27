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

// Initialize variable as nothing
let nvv = "";
let table = "";

$(document).ready(function() { 
    // Add plugin of DataTable to table of data
    table = $('#listado').DataTable({ 
        "dom": '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',    // Display order of objects of table
        "columns": [        // Define properties for the columns of the table 
            { "searchable": false, orderable: false },
            null,
            null,
            null,
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            null,
            null,
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
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
            $('.nuevo_comprobante_submit').prop('disabled', true);
            $('.nuevo_comprobante_submit').hide();
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
            row.child( format(data) ).show();
            tr.addClass('shown');
            $('#id_nvv_for_submit').val(row.data()[1]);
        }
    });
    
});

// If file is uploaded, show its name and enable button
function enable_button(){
    $('.nuevo_comprobante_submit').prop('disabled', false);
    $('.nuevo_comprobante_submit').show();

    let file = $('#id_nuevo_comprobante_pago').val();
    let name = file.split("\\");
    let nombre = name[name.length-1];
    if (file != null) {
        $('#file_name').html(nombre);
    }
}

// For showing the child data
function format (d) {
    var n_guia = '';
    var comprobante = '<td>' + $('#form_div').html() +'</td>';;
    // Choses which button to show depending on if order is ready or not, and also if it must show the guide number or not
    rowspan = 2;
    if (d[9] == 1) {
        n_guia = '<tr class="child_table">'+
            '<td>Número de guía:</td>'+
            '<td>' + d[6] + '</td>' +
        '</tr>'
        rowspan = 3;
        comprobante = '';
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
                '<td>' + 
                    d[5] + 
                '</td>' +
            '</tr>'+
            '<tr class="child_table">'+
                '<td>Cliente:</td>'+
                '<td>'+d[2]+'</td>'+
                '<td></td>'+
                comprobante +
            '</tr>'+
            '<tr class="child_table">'+
                '<td>RUT Cliente:</td>'+
                '<td>' + d[3] + '</td>'+
                '<td rowspan="' + (rowspan+2) + '" style="vertical-align: top;">Obervaciones del pedido:</td>'+
                '<td rowspan="' + (rowspan+2) + '" style="vertical-align: top;">' + d[10] + '</td>'+
            '</tr>'+
            '<tr class="child_table">' +
                '<td rowspan="' + rowspan + '" style="vertical-align: top;">Obervaciones solicitud:</td>'+
                '<td rowspan="' + rowspan + '" style="vertical-align: top;">' + d[12] + '</td>'+
            '</tr>' +
            '<tr class="child_table"></tr>' +
            '<tr class="child_table"></tr>' +
            n_guia +
        '</table>'+
    '</td>';
}