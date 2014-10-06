$(document).ready(function() {

    // Validate form
    $("#id_form_ad").submit(function() {
        var $this = $(this);

        var category = $this.find("input:radio").filter(':checked');

        if($("div." + category.attr('id')).length())
            return false;
    });

    // Dropdown
    $("#category label").click(function() {
        var $this = $(this);
        var parent = String($('div.id_category_' + $this.attr('data-parent')).attr('class')).split('parent-')[1];
        var label = $("label[for=id_category_" + parent + "]");

        $("#category div.dropdown-nav").hide();
        $("#category label").removeClass("active");

        $this.addClass('active');
        $this.parent('div.dropdown-nav').show();

        $("div." + $this.attr("for")).show();

        $("div.id_category_" + parent).show();
    });


    // Radio category
    $('#category .radio-category, select#id_category').change(function() {
        var $this = $(this);

        $.ajax({
            url: '/anuncios/category_meta/<pk>/'.replace('<pk>', $this.val()),
            type: 'GET',
            dataType: 'html',
            statusCode: {
                200: function(data) {
                    $("#metaoptions").html(data);
                },
                404: function(data) {
                    $("#metaoptions").html("");
                }
            }
        });
    });

    $("#id_form_offer").submit(function() {
        var $this = $(this);

        $.ajax({
            url: $this.attr('action'),
            type: 'POST',
            data: $this.find('input, textarea'),
            dataType: 'json',
            statusCode: {
                200: function(data) {
                    if(data.ok == 'true')
                        $("div#formOffer form div").html(data.html);
                        $.delay(2000).("div#formOffer").removeClass('in');

                    $("div#formOffer form div").html(data.html);
                }
            }
        });

        return false;
    });
});
