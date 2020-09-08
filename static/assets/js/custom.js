/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

"use strict";

function showEditPopup(triggeringLink) {
    let href = triggeringLink.href;
    let parts = href.split('/');
    let lastSegment = parts[parts.length - 1];
    let name = $("#"+lastSegment+" :selected").val();
    parts[parts.length - 2] = name;
    let newurl = parts.join("/");
    let win = window.open(newurl, "Edit",
       'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function showAddPopup(triggeringLink) {
    let href = triggeringLink.href;
    let win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function closePopup(win, newID, newRepr, id) {
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>');
    win.close();
}

function search() {
    $.ajax({
        type: "GET",
        data: {
            'q' : $('#search').val(),
            'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: searchSuccess,
        dataType: 'html'
    });
}

function _highlight_element(tag, text)
{
    let innerHTML = tag[0].innerHTML;
    let chunks = text.split(' ');
    for (let i = 0; i < chunks.length; i++) {
        text = chunks[i];
        if (!text) continue;
        let index = innerHTML.indexOf(text);
        let startIndex = 0;
        let insertion = "<mark>" + text + "</mark>";
        let searchStrLen = insertion.length;
        while ((index = innerHTML.toUpperCase().indexOf(text.toUpperCase(), startIndex)) > -1) {
            innerHTML = innerHTML.substring(0, index) + "<mark>" + innerHTML.substring(index, index + text.length) + "</mark>" + innerHTML.substring(index + text.length);
            startIndex = index + searchStrLen;
        }
        tag[0].innerHTML = innerHTML;
    }
}

function search_highlight(tag, text) {
        if (!text)
            return;
        if (tag.nodeName === 'A' || tag.nodeName ==='BUTTON')
            return;
        let head = $(tag);
        let ch_array = head.children();
        if (ch_array.length > 0)
            for(let i=0; i< ch_array.length; i++)
                search_highlight(ch_array[i], text)
        else
            _highlight_element(head, text);
    }
