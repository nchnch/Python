$(document).ready(function() {
    // Create params dialog
    $("#acc").dialog({
        bgiframe: true,
        autoOpen: false,
        height: 600,
        width: 900,
        modal: true,
        buttons:{ 'Отмена (Выбор параметров будет сохранен)': function() {
            $(this).dialog('close');
        },
            'Выбрать': function() {
                document.allpf.submit();
            }
        }
    });
    $("#acc").removeClass('display');

    $("input[name=allParamsDialog]").click(function() {
        //todo: CHECK ALL SELECTED
        $("#acc").dialog('open');
    });

    // Disabled copy for blocks
    var xx = document.getElementsByName("nocopydiv");
    for (var i = 0; i < xx.length; i++) {
        preventSelection(xx[i]);
    }

    // Next init script
    $(".lazyload_ad").lazyLoadAd({
        forceLoad: true
    });

})
