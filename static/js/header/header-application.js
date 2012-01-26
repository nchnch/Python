function loadBanners(timeout) {
    var Entries;
    $.getJSON('/bannerChooser', function(data){
        showBanners(data, timeout);
    });
}

function showBanners(data, timeout) {
    var Entries = data.entries,
    $ah = $('#ah-application'),
    $body = $(document.body),
    entryWidth = 180,
    buttonWidth = 21,
    interval, ahHover = false;

	if($.browser.msie) {$body.addClass('ie');}

	if($.browser.msie && $.browser.version < 8) {$body.addClass('ie7');}

    $ah.hover( function() {
        ahHover = true;

    }, function() {
        ahHover = false;
    });

    var initAhApplication = function() {
        clearInterval(interval);
        $ah.empty();

        var bodyWidth = $body.innerWidth(),
            perPage = Math.floor(bodyWidth/entryWidth),
            $entries = $("<div class='ah-entries'/>").appendTo($ah);

        if(perPage >= Entries.length) {
            $.each(Entries, function() {
                var Entry = this,
                $entry = $("<div class='ah-entry'/>")
                .css("background-image", "url("+Entry.img+")")
                .appendTo($entries);

                $("<a class='ah-entry-a' href='" + Entry.url +
                   "'target='_blank' onClick='recLinkExt(\"Баннер: " + Entry.title +
                    "\");extCl(this.href);window.open(this.href);return false;' id='external' ><span>Перейти</span></a>").appendTo($entry);
                $("<div class='ah-helper'></div>").appendTo($entry);
                $("<div class='ah-popup'>\
                    <div class='ah-popup-arr'></div>\
                    <div class='ah-popup-text'>\
                        <div class='ah-popup-title'>"+Entry.title+"</div>\
                        <div>"+Entry.text+"</div>\
                    </div>\
                </div>").appendTo($entry);
            });

            return;
        }

        var $paginator = $("<div class='ah-paginator'/>").appendTo($ah),
            $buttons = $("<div class='ah-paginator-buttons'/>").appendTo($paginator),
            $activeButton = $(),
            motion = false;

        interval = setInterval( function() {
            if(ahHover) { return };

            $buttonNext.trigger('click');
        }, 9977);

        var
            pageLength =Math.ceil(Entries.length/perPage)
            $buttonPrev = $("<a href='#'>&laquo;</a>").appendTo($buttons),
            $buttonNext = $("<a href='#'>&raquo;</a>"),
            buttons = {};

        for(var c = 1; c <= pageLength; c++) {

            var page = c, $button = buttons[c] =  $("<a href='#'/>")
                .attr('data-page', c)
                .text(c).appendTo($buttons)
                .bind("click", function(e) {
                    e.preventDefault();
                    renderPage($(this).attr('data-page'));
                });
        }

        $buttonNext.appendTo($buttons);
        $buttons.css('width', (pageLength+2)*buttonWidth);
        var half = $body.innerWidth() / 2. - (pageLength+2)*buttonWidth / 2.;
        $('.ah-paginator').css('left', half);

        $buttonPrev.bind('click', function(e) {
            e.preventDefault();
            var current = $activeButton.attr('data-page');

            if(current >= pageLength)
                renderPage(1);

            else
                renderPage(+current+1);
        });

       $buttonNext.bind('click', function(e) {
            e.preventDefault();
            var current = $activeButton.attr('data-page');

            if(current == 1)
                renderPage(pageLength);

            else
                renderPage(current-1);
        });

        var renderPage = function(pageIndex) {
            if(motion) return;

            motion = true;
            clearInterval(interval);
            $entries.animate({"opacity":0}, 550, function() {
                $entries.empty();
                interval = setInterval( function() {
                    if(ahHover) { return };

                    $buttonNext.trigger('click');
                }, 9977);

                var from = perPage*(pageIndex-1), to = from+perPage;

                if(to > Entries.length) {
                    to = Entries.length;
                }

                for(var i = from; i < to; i++) {
                    var Entry = Entries[i],
                    $entry = $("<div class='ah-entry'/>")
                    .css("background-image", "url("+Entry.img+")")
                    .appendTo($entries);

                    $("<a class='ah-entry-a' href='" + Entry.url +
                       "'target='_blank' onClick='recLink(\"Баннеры в шапке\", \"Баннер: " + Entry.title +
                        "\");extCl(this.href);window.open(this.href);return false;' id='external' ><span>Перейти</span></a>").appendTo($entry);
                    $("<div class='ah-helper'></div>").appendTo($entry);
                    $("<div class='ah-popup'>\
                        <div class='ah-popup-arr'></div>\
                        <div class='ah-popup-text'>\
                            <div class='ah-popup-title'>"+Entry.title+"</div>\
                            <div>"+Entry.text+"</div>\
                        </div>\
                    </div>").appendTo($entry);
                }

                $activeButton.removeClass("active");
                $activeButton = buttons[pageIndex].addClass("active");

                $entries.animate({'opacity': 1}, 750, function() {
                    motion = false;
                });
            });
        }

        renderPage(1);
    };

    initAhApplication();

    $(window).resize( function() { initAhApplication() });
}

// $(function() {
loadBanners(5000);
// });
