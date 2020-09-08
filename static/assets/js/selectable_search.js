"use strict";

function get_searchable_id(hid, inp, option_list, search_url) {
    let g = $(inp).val();
        $.ajax(search_url,{
        type: "GET",
        data: {
            'q' : g,
            'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function (data, textStatus, jqXHR) {
            $(option_list).html(data);
        },
        dataType: 'html'
    });
    let option_id = $(option_list).attr("id");
    let option = $('#'+option_id+' option[value="' + g +'"]')[0];
    if (option)
        $(hid).val(option.id);
    else
        $(hid).val(null);
}