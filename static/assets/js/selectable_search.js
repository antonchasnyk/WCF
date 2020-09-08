"use strict";

$( document ).ready(binder())

function binder(){
    let inp = document.getElementById('browser')
    inp.addEventListener('input', get_searchable_id);
}
function get_searchable_id() {
    let g = $('#browser').val();
    let option = $('#browsers option[value="' + g +'"]')[0];
    if (option)
    {
        console.log(option.id)
    }
}