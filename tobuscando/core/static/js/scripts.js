$(document).ready(function() {

    $("input[name*=price]").maskMoney({
        symbol: "R$",
        decimal: ",",
        thousands: "."
    });
    $('input[name*="date"]').datepicker({
        'format': 'dd/mm/yyyy',
        'language': 'pt-BR'
    });

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
