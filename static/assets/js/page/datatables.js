"use strict";

$("[data-checkboxes]").each(function() {
  var me = $(this),
    group = me.data('checkboxes'),
    role = me.data('checkbox-role');

  me.change(function() {
    var all = $('[data-checkboxes="' + group + '"]:not([data-checkbox-role="dad"])'),
      checked = $('[data-checkboxes="' + group + '"]:not([data-checkbox-role="dad"]):checked'),
      dad = $('[data-checkboxes="' + group + '"][data-checkbox-role="dad"]'),
      total = all.length,
      checked_length = checked.length;

    if(role === 'dad') {
      if(me.is(':checked')) {
        all.prop('checked', true);
      }else{
        all.prop('checked', false);
      }
    }else{
      if(checked_length >= total) {
        dad.prop('checked', true);
      }else{
        dad.prop('checked', false);
      }
    }
  });
});

$("#table-1").dataTable({
  "columnDefs": [
    { "sortable": false, "targets": [2,3] }
  ]
});
$("#table-2").dataTable({
 "columnDefs": [
    { "sortable": false, "targets": [0,2,3] }
  ],
  order: [[ 1, "asc" ]] //column indexes is zero based
  
});
$('#save-stage').DataTable({
		"scrollX": true,
		stateSave: true
	});

function formatDate(date, format) {
    const map = {
        mm: ('0' + (date.getMonth() + 1)).slice(-2),
        dd: ('0' + date.getDate()).slice(-2),
        yy: date.getFullYear().toString().slice(-2),
        yyyy: date.getFullYear(),
        MM: ('0' + date.getMinutes()).slice(-2),
        HH: ('0' + date.getHours()).slice(-2),
    };
    return format.replace(/mm|dd|yy|yyy|HH|MM/gi, matched => map[matched]);
}

function get_bom_title() {
                    return 'BOM '+ document.title.split(':')[1] + ' ' + formatDate(new Date(), 'dd.mm.yyyy_HH.MM');
                }

$('#tableExport').DataTable({
		dom: 'Bfrtip',
        paging: false,
        ordering: false,
        searching: false,
		buttons: [
            {
                extend: 'pdf',
                title: get_bom_title(),
                exportOptions: {
                    columns: ':visible:not(.notexport)',
                    rows: ':visible:not(.notexport)',
                    pageSize: 'A4'
                }
            },
            {
                extend: 'excel',
                title: get_bom_title(),
                exportOptions: {
                    columns: ':visible:not(.notexport)',
                    rows: ':visible:not(.notexport)'
                }
            },
            {
                extend: 'csv',
                title: get_bom_title(),
                exportOptions: {
                    columns: ':visible:not(.notexport)',
                    rows: ':visible:not(.notexport)'
                }
            },
            {
                extend: 'print',
                title: get_bom_title(),
                exportOptions: {
                    columns: ':visible:not(.notexport)',
                    rows: ':visible:not(.notexport)'
                }
            }
		]
	});
	