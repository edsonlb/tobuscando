$(document).ready(function() {
    $('#category .radio-category').click(function() {
        var $this = $(this);

        $.ajax({
            url: '/ads/category_meta/<pk>/'.replace('<pk>', $this.val()),
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
