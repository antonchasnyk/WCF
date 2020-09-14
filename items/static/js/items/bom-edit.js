'use strict';

$(function () {
	$('#id_add_new_form').on('click', add_new_form);
	$("#id_form_set").children('div').find("button").each(function(){ $(this).on('click', dell_row)});
});

function add_new_form() {
	let form_idx =$('#id_form-TOTAL_FORMS').val();
	$('#id_form_set').append($('#id_empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
}

function dell_row() {
	let row = $(this).parent().parent();
	$(row).find(':checkbox').val(true);
	$(row).find(':checkbox').prop('checked', true);
	console.log($(row).find(':checkbox').val())
    $(row).addClass('display-none');
}