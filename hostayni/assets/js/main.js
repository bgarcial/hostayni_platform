$(document).ready(function(i) {
    function o() {
        var o = i(".wrapper").width(),
            r = i(".search-column").width();
        i("main").width(o - r - 10)
    }

    function r() {
        var o = i(".wrapper").width(),
            r = i(".search-column").width(),
            t = i(".profile-info").width();
        i("#user-activity-main").width(o - r - t - 80)
    }
    var t = i(window).width();
    o(), r(), t < 1004 ? i("article").addClass("full-width-mobile") : i("article").removeClass("full-width-mobile"), i(window).resize(function() {
        t = i(this).width(), o(), r(), t < 1004 ? i("article").addClass("full-width-mobile") : i("article").removeClass("full-width-mobile")
    }), i("html").click(function() {
        i(".profile-options .options").find(".drop-down").hide(0)
    }), i(".profile-options .options").click(function(i) {
        i.stopPropagation()
    }), i(".profile-options .options").click(function() {
        i(this).find(".drop-down").slideToggle(150)
    }), i(".diary .button").on("click", function() {
        i(".diary .diary-drop-down").slideToggle(230)
    }), i("form #id_email").attr("placeholder", "Correo electrónico"), i("form #id_password1").attr("placeholder", "Contraseña"), i("form #id_password2").attr("placeholder", "Repetir contraseña"), i("form #id_full_name").attr("placeholder", "Nombre Completo"), i("form #id_username").attr("placeholder", "Nombre de usuario"), i("form #id_password").attr("placeholder", "Contraseña")
});