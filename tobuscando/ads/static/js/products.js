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

        $("#category label").removeClass("active");
        $this.addClass("active");

        $("div." + $this.attr("for")).show();
    });

    // Radio category
    $('#category .radio-category').click(function() {
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
});
