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
            $.post(url, {"option": option, "nvv": nvv});
        }
    })
})

$(document).ready(function() { 
    var table = $('#listado').DataTable({        
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
            // Open this row
            row.child( format(data) ).show();
            tr.addClass('shown');
        }
    } );
});

function format (d) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Fecha NVV:</td>'+
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
            '<td> Comprobante de pago:</td>' +
            '<td>' +
                d[4] +
            '</td>' +
        '</tr>' +
        '<tr>'+
            '<td>Obervaciones:</td>'+
            '<td>' + d[5] + '</td>'+
        '</tr>'+
    '</table>';
}
 