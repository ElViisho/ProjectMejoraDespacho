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
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth() + 1; //January is 0!
	var yyyy = today.getFullYear();

	if (dd < 10) {
	   dd = '0' + dd;
	}

	if (mm < 10) {
	   mm = '0' + mm;
	} 
		
	today = yyyy + '-' + mm + '-' + dd;
	$('.fecha_despacho').prop("min", today);

    //Custom ordering for dates
	(function () {
 
        var customDateDDMMMYYYYToOrd = function (date) {
            "use strict"; //let's avoid tom-foolery in this function
            // Convert to a number YYYYMMDD which we can use to order
            var dateParts = date.split(' ');
            return (dateParts[2] * 10000) + ($.inArray(dateParts[1], ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]) * 100) + (dateParts[0]*1);
        };
         
        // This will help DataTables magic detect the "dd-MMM-yyyy" format; Unshift
        // so that it's the first data type (so it takes priority over existing)
        jQuery.fn.dataTableExt.aTypes.unshift(
            function (sData) {
                "use strict"; //let's avoid tom-foolery in this function
                if (/^([0-2]?\d|3[0-1]) (enero|febrero|marzo|abril|Mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) \d{4}/i.test(sData)) {
                    return 'date-dd-mmm-yyyy';
                }
                return null;
            }
        );
         
        // define the sorts
        jQuery.fn.dataTableExt.oSort['date-dd-mmm-yyyy-asc'] = function (a, b) {
            "use strict"; //let's avoid tom-foolery in this function
            var ordA = customDateDDMMMYYYYToOrd(a),
                ordB = customDateDDMMMYYYYToOrd(b);
            return (ordA < ordB) ? -1 : ((ordA > ordB) ? 1 : 0);
        };
         
        jQuery.fn.dataTableExt.oSort['date-dd-mmm-yyyy-desc'] = function (a, b) {
            "use strict"; //let's avoid tom-foolery in this function
            var ordA = customDateDDMMMYYYYToOrd(a),
                ordB = customDateDDMMMYYYYToOrd(b);
            return (ordA < ordB) ? 1 : ((ordA > ordB) ? -1 : 0);
        };
         
        })();
	
	
    // Add plugin of DataTable to table of data
    table = $('#listado').DataTable({ 
        "dom": '<"top"iflp<"clear">>rtB<"bottom"iflp<"clear">>',    // Display order of objects of table
        "columns": [        // Define properties for the columns of the table 
            { "searchable": false, orderable: false },
            null,
            null,
            null,
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            null,
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
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
            { "searchable": false, orderable: false, render: function (data, type, row) {
                x = []
                for (i in data){
                    switch(data[i]){
                        case "0": x.push("No asignado"); break;
                        case "1": x.push("AM"); break;
                        case "2": x.push("PM"); break;
                        default: x.push(""); break;
                    }
                }
                return x;
                }
            },
            { "searchable": false, orderable: false, render: function (data, type, row) {
                x = []
                for (i in data){
                    switch(data[i]){
                        case "0": x.push("En preparación"); break;
                        case "1": x.push("Sin pago adjunto"); break;
                        case "2": x.push("Sin material"); break;
                        case "3": x.push("Preaparado incompleto"); break;
                        case "4": x.push("Preaparado completo"); break;
                        default: x.push(""); break;
                    }
                }
                return x;
                } },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
        ],
        columnDefs: [
            { type: 'date-dd-mmm-yyyy', targets: [2] }
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
                    columns: [ 0, 1, 2, 3, 4, 5, 17, 8, 12, 13, 14, 15, 18, 16],
                    format: {
                        body: function ( data, row, column, node ) {
                            // Format date for excel
                            if (column === 2 ) {
								if (data == 'No asignada') return data;
                                d = data.split(' ');
								var mes="";
                                switch(d[1]){
                                    case "Enero": mes = "01"; break;
                                    case "Febrero": mes = "02"; break;
                                    case "Marzo": mes = "03"; break;
                                    case "Abril": mes = "04"; break;
                                    case "Mayo": mes = "05"; break;
                                    case "Junio": mes = "06"; break;
                                    case "Julio": mes = "07"; break;
                                    case "Agosto": mes = "08"; break;
                                    case "Septiembre": mes = "09"; break;
                                    case "Octubre": mes = "10"; break;
                                    case "Noviembre": mes = "11"; break;
                                    case "Diciembre": mes = "12"; break;
									default: mes=""; break;
                                }
                                return d[0]+"-"+mes+"-"+d[2];
                            }
                            else if (column === 6) {
                                d = data.split(' ');
								var mes="";
                                switch(d[2]){
                                    case "Enero": mes = "01"; break;
                                    case "Febrero": mes = "02"; break;
                                    case "Marzo": mes = "03"; break;
                                    case "Abril": mes = "04"; break;
                                    case "Mayo": mes = "05"; break;
                                    case "Junio": mes = "06"; break;
                                    case "Julio": mes = "07"; break;
                                    case "Agosto": mes = "08"; break;
                                    case "Septiembre": mes = "09"; break;
                                    case "Octubre": mes = "10"; break;
                                    case "Noviembre": mes = "11"; break;
                                    case "Diciembre": mes = "12"; break;
									default: mes=""; break;
                                }
                                return d[0]+"-"+mes+"-"+d[4];
                            }
                            return data;
                        }
                    }
                },
                title: "Ordenes de despacho",
                customize: function(xlsx) {
                    var styleSheet = xlsx.xl['styles.xml'];
                    var lastXfIndex = $('cellXfs xf', styleSheet).length - 1;
                    var n1 = '<numFmt formatCode="$ #,##0" numFmtId="300"/>';
                    var s1 = '<xf numFmtId="300" fontId="0" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1" xfId="0" applyNumberFormat="1"/>';
                    var n2 = '<numFmt formatCode="dd-mm-yyyy" numFmtId="302"/>';
                    var s2 = '<xf numFmtId="302" fontId="0" fillId="0" borderId="0" applyFont="1" applyFill="1" applyBorder="1" xfId="0" applyNumberFormat="1"/>';
                    styleSheet.childNodes[0].childNodes[0].innerHTML += n1;
                    styleSheet.childNodes[0].childNodes[5].innerHTML += s1;
                    styleSheet.childNodes[0].childNodes[5].innerHTML += s1;
                    styleSheet.childNodes[0].childNodes[5].innerHTML += s2;

                    var currencyFormat = lastXfIndex + 1;
                    var dateFormat = lastXfIndex + 2;
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="J"]', sheet).attr( 's', currencyFormat );
                    $('row c[r="J2"]', sheet).attr( 's', '2' );
                    $('row c[r^="C"]', sheet).attr( 's', dateFormat );
                    $('row c[r="C2"]', sheet).attr( 's', '2' );
                    $('row c[r^="G"]', sheet).attr( 's', dateFormat );
                    $('row c[r="G2"]', sheet).attr( 's', '2' );
                }
            }
        ]
    });    

    // When + symbol or NVV value is clicked, it shows all the relevant info
    $('#listado tbody').on('click', 'td.show_hide', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var data = row.data()[11].split("\\,\\,")
        data.push(row.data()[16])
        data.push(row.data()[13])
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
            $('#id_nvv_for_submit').val(row.data()[1]);
        }
    } );

    // If user has permissions
    if (permissions == 'Despacho') {
        // Post to change the state of the order
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

        // Post to change the hour range of the order
        $('.rango_horario').on('change', function () {
            var url = window.location.href;
            var option = $(this).val();
            var nvv = this.id;

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

            $.ajax({
                success: function () {
                    $.post(url, {"type": "rango_horario", "nvv": nvv, "option": option,}),
                    table.cell('#rango_horario' + nvv).data(option)
                }
            })
        })

        // Post to change the state of the order for the seller
        $('.estados_pedido_para_vendedor').on('change', function () {
            var url = window.location.href;
            var option = $(this).val();
            var nvv = this.id;

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

            $.ajax({
                success: function () {
                    $.post(url, {"type": "estado_pedido_para_vendedor", "nvv": nvv, "option": option,}),
                    table.cell('#estado_pedido' + nvv).data(option)
                }
            })
        })

        // Post to change the state of the order for the seller
        $('.fecha_despacho').on('change', function () {
            var url = window.location.href;
            var date = $(this).val();
            var nvv = this.id;

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

            $.ajax({
                success: function () {
                    $.post(url, {"type": "fecha_despacho", "nvv": nvv, "date": date,})
                    table.cell('#fecha_despacho_final' + nvv).data(date)
                }
            })
        })
    }

    $('.despacho_externo').html(function() {
        arr = $(this).html().split('\\');
        if (!arr[1]) return 'DIMACO';
        return '<i>' + arr[0] + '</i><br>' + arr[1];
    })
});

function textAreaChange() {
    var url = window.location.href;
    var textArea = document.getElementsByClassName('observaciones_pedido')[0];
    var nvv = textArea.id;
    var observaciones = textArea.value;
    
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        success: function () {
            // Post to change the observations of the order
            $.post(url, {"type": "observaciones_pedido", "nvv": nvv, "observaciones": observaciones,})
            table.cell('#observacion_despacho' + nvv).data(observaciones)
        }
    })
}

function dateChange(picker) {
    // Add listener to date picker to check if day selected is not weekend
    // and alert user if that's the case
    const initialDate = picker.defaultValue;
    const min = picker.min;
    var day = new Date(picker.value).getUTCDay();
    if([6,0].includes(day) || picker.value<min){
        picker.value=initialDate;
        alert('Fecha inválida');
    }
}

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

// Initialize variable as 0 (falsey)
var listo = 0;

// For showing the child data
function format (d) {
    var n_guia = '';
    var comprobante = '';
    // Choses which button to show depending on if order is ready or not, and also if it must show the guide number or not
    listo = d[10];
    if (d[10] == 1) {
        n_guia = '<tr class="child_table">'+
            '<td>Número de guía:</td>'+
            '<td>' + d[7] + '</td>' +
            '<td>Voucher de despacho:</td>' + 
            '<td>' + d[13] +'</td>' +
        '</tr>'
        comprobante = '<tr class ="child_table">'+
                        '<td></td>'+
                        '<td></td>'+
                        '<td></td>'+
                        '<td>' + $('#form_div').html() +'</td>' +
                    '</tr>';
        boton_guia_despacho = "Borrar número de guía";
    }
    else boton_guia_despacho = "Marcar como despachado";

    // If user doesn't have permission, don't show button
    var boton_despacho = '';
    if (permissions == 'Despacho') {
        boton_despacho = '<tr class="child_table">'+
            `<td colspan='2' style='text-align: center'><input class="btn btn-default boton-sumbit" onclick="prompt_confirm(${listo})" id="boton" value="${boton_guia_despacho}" readonly></td>` +
        '</tr>';
    }
    
    // Child table for extra data
    return '<td class="child_table">' + 
        '<table cellpadding="5" cellspacing="0" border="0">'+
            '<tr class="child_table">' +
                '<td>Nombre vendedor:</td>' +
                '<td>' + d[8] + '</td>' +
                '<td>Valor neto:</td>' +
                '<td>$' + Number(d[15]).toLocaleString() + '</td>' + 
            '</tr>' +
            '<tr class="child_table">' +
                '<td>Solicitado por:</td>' +
                '<td>' + d[9] + '</td>' +
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
                '<td rowspan="2" style="vertical-align: top;">Obervaciones solicitud:</td>'+
                '<td rowspan="2" style="vertical-align: top;">' + d[6] + '</td>'+
            '</tr>'+
            '<tr class="child_table">'+
                '<td>RUT Cliente:</td>'+
                '<td>' + d[3] + '</td>'+
            '</tr>'+
            '<tr class="child_table">'+
                '<td>Nombre Contacto:</td>'+
                '<td>' + d[11] + '</td>'+
                '<td rowspan="2" style="vertical-align: top;">Observaciones del pedido:</td>' +
                '<td rowspan="2" style="vertical-align: top;"><textarea onchange="textAreaChange()" class="observaciones_pedido" id="'+ d[0] +
                    '" style="resize:none" rows=3 cols=50 placeholder="Ingrese alguna observación en caso de ser pertinente">' + d[14] + '</textarea></td>' +
            '</tr>'+
            '<tr class="child_table">'+
                '<td>Teléfono Contacto:</td>'+
                '<td>' + d[12] + '</td>'+
            '</tr>'+
            n_guia +
            comprobante +
            boton_despacho +
        '</table>' +
    '</td>';
}

// The prompt for confirmation of changes on table
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
            $('#boton_confirm').hide();
            $('#boton_cancel').hide();
            document.getElementById('confirm_texto').style.marginBottom = '25px';
        },
        data: {"type": "numero_guia", "nvv": nvv, "listo": listo},
        success: function () {
			// Prompt the user the success and after 1 second reload table
            $('#confirm_texto').html('Éxito. La página se recargará en breve.');
            setTimeout('window.location.reload()', 1000);
        },
        error: function () {
            // Prompt the user there was no guide number and after 2 seconds reload table
            $('#confirm_texto').html('Error. Orden no tiene documento asociado. La página se recargará en breve.');
            setTimeout('window.location.reload()', 2000);
        },
        timeout: 5000 
    })

}

// The prompt for confirmation of changes on table
function prompt_confirm_file() {
    $('#confirm_texto_file').html(`¿Confirmas que quieres subir un nuevo voucher de despacho para la orden ${$('#id_nvv_for_submit').val()}? (Esto eliminará el anterior en caso de existir)<br>`);
    $('#confirm_prompt_background_file').show();
    $('#confirm_prompt_file').show();
    $('#confirm_texto_file').show();
    $('#boton_confirm_file').show();
    $('#boton_cancel_file').show();
}

// Function to cancel the deletion
function cancelar_file() {
    $('#confirm_prompt_background_file').hide();
    $('#confirm_prompt_file').hide();
    $('#confirm_texto_file').hide();
    $('#boton_confirm_file').hide();
    $('#boton_cancel_file').hide();
}