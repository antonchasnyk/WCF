'use strict';
$(function () {
    $('#editParameters').editableTableWidget();
    $('#id_row_add').on('click', add_row);
    $("#editParameters").children('tbody').find("button").each(function(){ $(this).on('click', dell_row)});
    $("#id_parameters_save").on('click', save_table)
});

function add_row() {
    let row_count = parseInt($('#id_row_counts').val())+1;
    let table = $('#editParameters');
    let table_body = table.children('tbody');
    let row = table_body.append( ' <tr>\n' +
        '<td id="'+row_count+'"></td>\n' +
        '<td id="'+row_count+'"></td>\n' +
        '<th id="'+row_count+'"><button class="btn btn-danger" id="id_row_delete" >' +
        '<i class="fas fa-times"></i></button></th>\n' +
        '</tr>');
    row.children(':last').children('th').children('button').on('click', dell_row);
    $('#id_row_counts').val(row_count);
    table.editableTableWidget();
}

function dell_row() {
    $(this).parent().parent().remove();
    let row_count = parseInt($('#id_row_counts').val()) - 1;
    $('#id_row_counts').val(row_count);
    $('#editParameters').editableTableWidget();
}

function save_table() {
    let table_body = $('#editParameters').children('tbody');
    let to_json = {};
    $(table_body).find("tr").each(function () {
        let data_row = $(this).find('td');
        let key = $(data_row[0]).text();
        let data = $(data_row[1]).text();
        if(key !== '' && data !=='')
        {
            to_json[key] =data;
        }
        else
            $(this).remove();
    });
    console.log(JSON.stringify(to_json));
    let target = $('#id_parameters_save').attr('href');
    $.ajax(target, {
        type: "POST",
        data: {
            'parameters' : JSON.stringify(to_json),
            'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success:function(data){
                        iziToast.success({
                        title: data,
                        position: 'topRight',
                        timeout: 10000,
                    })},
        error: function (jqXHR, exception) {
            iziToast.error({
                                title: jqXHR.responseText,
                                position: 'topRight',
                                timeout: 10000,
                            })
        },
        dataType: 'html'
    });
}