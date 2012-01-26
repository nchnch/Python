/* Перемещаем div id="box_txt" в самаый подвал перед div class"foot" */

$(window).ready(function() {
    $("#box_txt").prependTo($("#footer"));
});



/* Выпадающий список для доп. функций */

$(window).ready(function() {
    if (typeof game_page == 'object') {
        game_page.moreDrop();
        game_page.popup();
    }
});

var game_page = {};

game_page.moreDrop = function() {
    var $more = $('#cont .game li.more');
    var $slot = $('#cont .game');

    $more.each(function() {
        var $dropdown = $('.dropdown', $(this));

        $(this).click(function(e) {
            if ($('a', $(this)).hasClass('active')) {
                $('a', $(this)).removeClass('active');
                $dropdown.hide();
            } else {
                $('a', $(this)).addClass('active');
                $dropdown.show();
            }
            e.preventDefault();
        });
    });

    $slot.each(function() {
        var $more = $('li.more a', $(this));
        var $dropdown = $('li.more .dropdown', $(this));

        $('.dropdown').mouseleave(function() {
            $more.removeClass('active');
            $dropdown.hide();
        })
    });

};

game_page.popup = function() {
    var $open = $('#filtr a.popup_more');
    var $close_1 = $('#popup_overlay');
    var $close_2 = $('.popups a');
    var $win = $('#win');
    var $overlay = $('#popup_overlay');

    $open.click(function() {
        $overlay.show();
        $win.show();
        $('#page').css("overflow", "hidden");
    });

    $close_1.click(function() {
        $overlay.hide();
        $win.hide();
        $('#page').css("overflow", "auto");
    });

    $close_2.click(function() {
        $overlay.hide();
        $win.hide();
        $('#page').css("overflow", "auto");
    });
};



/*Главное меню залипает в вверху страницы при скроллинге контента,
 так же есть ссылка на скрытие поиска
 так же опускаем лифт или поднимаем
 */

$(window).scroll(function() {
    var scroll_top = $(window).scrollTop();

    if (scroll_top >= 225) {
        $("#main_menu_search").addClass("search_fix");
        $("#lift ul").addClass("lift_fix");
        $("#box_lift").addClass("box_lift_fix");
    }else {
        $("#main_menu_search").removeClass("search_fix");
        $("#lift ul").removeClass("lift_fix");
        $("#box_lift").removeClass("box_lift_fix");
    }
});

function hide_search() {

    var scroll_top = $(window).scrollTop();

    if (scroll_top >= 225) {
        $("#main_menu_search").hide();
        $(".show_search").show();
        $("#lift ul").addClass("lift_fix_hide");
        $("#box_lift").addClass("box_lift_fix_hide");
    }
}

function show_search() {
    $("#main_menu_search").show();
    $(".show_search").hide();
    $("#lift ul").removeClass("lift_fix_hide");
    $("#box_lift").removeClass("box_lift_fix_hide");
}

$(window).scroll(function() {

    var scroll_top = $(window).scrollTop();

    if (scroll_top < 225) {
        $("#main_menu_search").show();
        $(".show_search").hide();
        $("#lift ul").removeClass("lift_fix_hide");
        $("#lift ul").removeClass("lift_fix");
        $("#box_lift").removeClass("box_lift_fix_hide");
        $("#box_lift").removeClass("box_lift_fix");
    }
});



/*Размещение 3-х колонок контента, при разной ширине окна,
 будут разные размеры колонок и отображене колонки #link
 */

function coll_game() {

    var bw = $(window).width();
    var link = $("#link");
    var cont = $("#cont");
    var lift = $("#lift");
    var ul_game = $(".games_page");

    var ul_padd_1 = Math.round((bw - 1000)/2);
    var ul_padd_2 = Math.round((bw - 1201)/2);
    var ul_padd_3 = Math.round((bw - 1361)/2);
    var ul_padd_4 = Math.round((bw - 1621)/2);

    /*4 игры в ряд и лифт, ссылки НЕ видно*/
    if (bw <= 1200) {
        cont.width(885);
        link.hide();
    }
    if (bw >= 1001 && bw <= 1200) {
        ul_game.css("padding-left", ul_padd_1);
        ul_game.css("padding-right", ul_padd_1);
    }

    /*5 игр в ряд и лифт, ссылки НЕ видно*/
    if (bw >= 1201 && bw <= 1360) {
        cont.width(1105);
        link.hide();
    }
    if (bw >= 1201 && bw <= 1360) {
        ul_game.css("padding-left", ul_padd_2);
        ul_game.css("padding-right", ul_padd_2);
    }

    /*5 игр в ряд и лифт, ссылки видно*/
    if (bw >= 1361 && bw <= 1620) {
        cont.width(1105);
        link.show();
    }
    if (bw >= 1361 && bw <= 1620) {
        ul_game.css("padding-left", ul_padd_3);
        ul_game.css("padding-right", ul_padd_3);
    }

    /*6 игр в ряд и лифт, ссылки видно*/
    if (bw >= 1621) {
        cont.width(1330);
        link.show();
    }
    if (bw >= 1621) {
        ul_game.css("padding-left", ul_padd_4);
        ul_game.css("padding-right", ul_padd_4);
    }
}



/*Работаем с лифтом, все что в него входит*/

//Определяем высоту лифта
function height_lift() {
    var hbw = $(window).height();
    var hc = $("#cont").height();
    var status = hc / hbw;
    var value_stage = ((status.toFixed(0)) * 20) + 1;
    var bl = $("#box_lift");

    bl.height(value_stage);
}

//Управление скроллирование по Y, с помощью лифта
function click_lift_top() {
    var scroll_y = $(window).scrollTop();
    scroll_y = scroll_y + 185;
    $(window).scrollTop(scroll_y);
}

function click_lift_bottom() {
    var scroll_y = $(window).scrollTop();
    scroll_y = scroll_y - 185;
    $(window).scrollTop(scroll_y);
}

//Измененния статуса, причем в метрах :), 1 метр = 1 высота окна браузера
function status_lift() {
    var hbw = $(window).height();
    var hc = $("#cont").height();
    var status = Math.round(hc / hbw);

    $(".score_lift").text(status);

    //Изменения окончания едениц, метр; метра; метров;

    if (status == 0 || (status >= 5 && status <= 20) || (status >= 25 && status <= 30) || (status >= 35 && status <= 40) || (status >= 45 && status <= 50) || (status >= 55 && status <= 60) || (status >= 65 && status <= 70) || (status >= 75 && status <= 80) || (status >= 85 && status <= 90) || (status >= 95 && status <= 100)) {
        $(".metr_lift").text("метров");
    } else if (status == 1 || status == 21 || status == 31 || status == 41 || status == 51 || status == 61 || status == 71 || status == 81 || status == 91 || status == 101 ) {
        $(".metr_lift").text("метр");
    } else if ((status >= 2 && status <= 4) || (status >= 22 && status <= 24) || (status >= 32 && status <= 34) || (status >= 42 && status <= 44) || (status >= 52 && status <= 54) || (status >= 62 && status <= 64) || (status >= 72 && status <= 74) || (status >= 82 && status <= 84) || (status >= 92 && status <= 94)) {
        $(".metr_lift").text("метрa");
    }
}

//Кабинка лифта, пусть ездит!
function win_cabin() {

    var x = 225;

    var wb = $("#box_lift").height();
    var p_wb = wb / 100;
    var st_bw_max = $("body").height();
    var ts = st_bw_max - x;
    var p_ts = ts / 100;

    var st_bw = $(window).scrollTop();
    var top = st_bw / p_ts;

    if (st_bw >= x) {
        $(".win_user").attr("style", "top:" + top + "px");
    } else if (st_bw <= x) {
        $(".win_user").attr("style", "top:0");
    }

    /*$("#debug").html(
     "Высота всего лифта " + wb + "px; <br/>"
     + "1% лифта, равен " + p_wb + "px; <br/>"
     + "MAX скролл страницы " + st_bw_max + "px; <br/>"
     + "Нужный сролл страницы " + ts + "px; <br/>"
     + "1% от нужного сролла, равен " + p_ts + "px; <br/>"
     + "---- <br/>"
     + "На данный момент, скролл " + st_bw + "px; <br/>"
     + "TOP будет равен " + top + "px."

     );*/

}



function debug() {

    var hl_d = $("#cont").height();
    var scroll_top = $(window).scrollTop();
    var height_bw = $(window).height();
    var width_bw = $(window).width();

    var hbw = $(window).height();
    var hc = $("#cont").height();
    var status = hc / hbw;

    var math = Math.round(190.29);

    /*$("#debug").html(
     "Высота контента " + hl_d + "px; <br/>"
     + "Проскролили " + scroll_top + "px; <br/>"
     + "Высота окна " + height_bw + "px; <br/>"
     + "Ширина окна " + width_bw + "px; <br/>"
     + "Кол-во моников " + status.toFixed(0) + "шт <br/>"
     + "Деление, без остатка " + math
     );*/
}

/*Запускаем функции*/

$(window).resize(function(){
    coll_game();
    height_lift();
    status_lift();
    win_cabin();
    debug();
});

$(window).scroll(function(){
    win_cabin();
    debug();
});

$(window).ready(function(){
    coll_game();
    height_lift();
    status_lift();
    win_cabin();
    debug();

    if (navigator.userAgent.indexOf("Firefox")!=-1)
    $("#one").ellipsis();
});

function popwin(url,name,options){
    var ContextWindow = window.open(url,name,options);
    ContextWindow.focus();
    return false;
}
