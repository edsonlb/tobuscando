$(document).ready(function() {

    $("input#id_price").maskMoney({
        symbol: "R$",
        decimal: ",",
        thousands: "."
    });
    $('input[name*="date"]').mask('99/99/9999');

    $("form#id_form_search").submit(function() {
        var $this = $(this);
        var search = $(this).find('input#id_search');
        var value = search.val().replace(' ', '-');

        if(value)
            window.location = '/busca/' + value + '/';

        search.focus();
        return false;
    });
});
