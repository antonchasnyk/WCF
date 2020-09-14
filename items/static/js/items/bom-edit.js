'use strict';

$(function () {
    console.log(parseInt($('#id_form-TOTAL_FORMS').val()))
      $('#id_add_new_form').on('click', add_new_form);
});

function add_new_form() {
	let form_idx =$('#id_form-TOTAL_FORMS').val();
	$('#id_form_set').append($('#id_empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
}