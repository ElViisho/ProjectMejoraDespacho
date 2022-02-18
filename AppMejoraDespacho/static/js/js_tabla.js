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
            return decodeURI(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}


function domDataTable() {
    if (permissions=='Eliminar') return '<"top"iflp<"clear">>rtB<"bottom"iflp<"clear">>'
    return '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>'
}

// Array with the name of months for display
const nombresMeses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

// Initialize variable as nothing
let nvv = "";
let table = "";

$(document).ready(function() {
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
        "dom": domDataTable(),    // Display order of objects of table
        "columns": [        // Define properties for the columns of the table 
            { "searchable": false, orderable: false },
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
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
            { "searchable": false, orderable: false },
        ],
		columnDefs: [
		   { type: 'date-dd-mmm-yyyy', targets: [2,8] }
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
        order: [ 7, 'asc' ],            // Default order by state
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
                    columns: [ 0, 1, 2, 17, 3, 4, 7, 14, 8, 9, 12, 15, 16],
                    format: {
                        body: function ( data, row, column, node ) {
                            // Format date for excel
                            if (column === 2 || column === 8) {
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
							else if (column === 7){
								d = data.split(' ');
								var mes="";
                                switch(d[0]){
                                    case "Ene.": mes = "01"; break;
                                    case "Feb.": mes = "02"; break;
                                    case "Mar.": mes = "03"; break;
                                    case "Abr.": mes = "04"; break;
                                    case "Mayo": mes = "05"; break;
                                    case "Jun.": mes = "06"; break;
                                    case "Jul.": mes = "07"; break;
                                    case "Ago.": mes = "08"; break;
                                    case "Sept.": mes = "09"; break;
                                    case "Oct.": mes = "10"; break;
                                    case "Nov.": mes = "11"; break;
                                    case "Dic.": mes = "12"; break;
									default: mes=""; break;
                                }
                                return d[1].slice(0,-1)+"-"+mes+"-"+d[2];
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
                    styleSheet.childNodes[0].childNodes[0].innerHTML += n2;
                    styleSheet.childNodes[0].childNodes[5].innerHTML += s1;
                    styleSheet.childNodes[0].childNodes[5].innerHTML += s2;

                    var currencyFormat = lastXfIndex + 1;
                    var dateFormat = lastXfIndex + 2;
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="J"]', sheet).attr( 's', currencyFormat );
                    $('row c[r="J2"]', sheet).attr( 's', '2' );
                    $('row c[r^="C"]', sheet).attr( 's', dateFormat );
                    $('row c[r="C2"]', sheet).attr( 's', '2' );
                    $('row c[r^="H"]', sheet).attr( 's', dateFormat );
                    $('row c[r="H2"]', sheet).attr( 's', '2' );
					$('row c[r^="I"]', sheet).attr( 's', dateFormat );
                    $('row c[r="I2"]', sheet).attr( 's', '2' );
                }
            }
        ]
    });

    // When + symbol or NVV value is clicked, it shows all the relevant info
    $('#listado tbody').on('click', 'td.show_hide', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var data = row.data()[10].split("\\,\\,")
        data.push(row.data()[12])
        data.push(row.data()[13])
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

    $('.despacho_externo').html(function() {
        arr = $(this).html().split('\\');
        return '<i>' + arr[0] + '</i><br>' + arr[1];
    })
    
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
    var comprobante = '<td>' + $('#form_div').html() +'</td>';
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



// Shows prompt for confirming if user wants to change the selected order's payment file
function prompt_confirm() {
    $('#confirm_texto').html(`¿Confirmas que quieres subir un nuevo comprobante de pago para la orden ${$('#id_nvv_for_submit').val()}? (Esto eliminará el anterior en caso de existir)<br>`);
    $('#confirm_prompt_background').show();
    $('#confirm_prompt').show();
    $('#confirm_texto').show();
    $('#boton_confirm').show();
    $('#boton_cancel').show();
}

// Function to cancel the deletion
function cancelar() {
    $('#confirm_prompt_background').hide();
    $('#confirm_prompt').hide();
    $('#confirm_texto').hide();
    $('#boton_confirm').hide();
    $('#boton_cancel').hide();
}