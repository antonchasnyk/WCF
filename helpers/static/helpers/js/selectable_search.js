"use strict";

let selectors = $("[href][name*='selector']:input");
for (let i=0; i<selectors.length; i++)
{
    let inp = selectors[i];
    let selector_id = inp.id.split("_");
    let hid = $("#"+selector_id[0]+"_"+selector_id[1])[0];
    let option_list = inp.list;
    let search_url = $(inp).attr('href');
    $(inp).on( 'input', function() {
      let g = $(inp).val();
        $.ajax(search_url,{
        type: "GET",
        data: {
            'q' : g,
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
    });
}