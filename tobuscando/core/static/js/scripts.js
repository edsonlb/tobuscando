$(document).ready(function() {

    $("ul#category_id li").mouseover(function() {
        $("ul#category_id li .dropdown-nav").hide();
        $(this).find(".dropdown-nav").show();
    })
});
