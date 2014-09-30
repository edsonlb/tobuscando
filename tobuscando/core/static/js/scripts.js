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

    $("input[name^=phone]").focusout(function(){
        var phone, element;
        element = $(this);
        element.unmask();
        phone = element.val().replace(/\D/g, '');

        if(phone.length > 10) {
            element.mask("(99) 99999-999?9");
        } else {
            element.mask("(99) 9999-9999?9");
        }
    }).trigger('focusout');

    $("form#id_form_search").submit(function() {
        var $this = $(this);
        var search = $(this).find('input#id_search');
        var value = search.val().replace(' ', '-');

        if(value)
            window.location = '/busca/' + value + '/';

        search.focus();
        return false;
    });

    $('input[name*=url').keyup(function() {
        var $this = $(this);
        var val = $this.val().replace('http://', '');

        $this.val('http://' + val);
    });
});
