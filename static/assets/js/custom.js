/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

"use strict";

$('.searchable').searchable();

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
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
    win.close();
}
