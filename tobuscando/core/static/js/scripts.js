$(document).ready(function() {

    $("input[name*=price]").maskMoney({
        symbol: "R$",
        decimal: ".",
        thousands: ""
    });

    $('input[name*=date]').datepicker({
        'format': 'dd/mm/yyyy',
        'language': 'pt-BR'
    }).mask('99/99/9999');

    $('input#id_zipcode').mask('99999-999');

    $("input#id_phone").mask("(99) 9999-9999");
    $("input#id_cellphone").mask("(99) 99999-9999");

    $("form#id_form_search").submit(function() {
        var $this = $(this);
        var search = $(this).find('input#id_search');
        var value = search.val().replace(' ', '-');

        if(value)
            window.location = '/busca/' + value + '/';

        search.focus();
        return false;
    });

    $('input#id_link').focus(function() {
        var $this = $(this);
        var val = $this.val();

        if (val == '')
            $this.val('http://' + val);
    });
});
