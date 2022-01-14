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
    $('#listado').DataTable({        
        "columns": [
            null,
            null,
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            null,
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            null,
            { "searchable": false, orderable: false },
            null,
            null,
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
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
        buttons: {
            buttons: [
                { extend: 'next', className: 'boton' },
                { extend: 'previous', className: 'boton' }
            ]
        },
    });
});

