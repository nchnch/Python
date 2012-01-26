
function selOptSearch() {
    selVal=$('#optSearch option:selected').val();
    if(selVal==1){
        $('#searchElements').html('<br><label><b>Домен или название казино:</b> </label><br><center><input id="search1" name="search1" type="text" onkeypress="return processKeyPress(event);" style="width: 100%" /></center>');
    }
    if(selVal==2){
        $('#searchElements').html('<br><label><b>Слово или фраза для поиска:</b> </label><br><center></center>');
    }
}

function isValidEmail() {
    var re = /^\w+([\.-]?\w+)*@(((([a-z0-9]{2,})|([a-z0-9][-][a-z0-9]+))[\.][a-z0-9])|([a-z0-9]+[-]?))+[a-z0-9]+\.([a-z]{2}|(com|net|org|edu|int|mil|gov|arpa|biz|aero|name|coop|info|pro|museum))$/i;
    var email=document.getElementsByName("email")[0].value;
    if(re.test(email))  return true;
    else {
        alert("Введен некорректный Email");
        return false;
    }
}

function isValidEmail1(value) {
    var re = /^\w+([\.-]?\w+)*@(((([a-z0-9]{2,})|([a-z0-9][-][a-z0-9]+))[\.][a-z0-9])|([a-z0-9]+[-]?))+[a-z0-9]+\.([a-z]{2}|(com|net|org|edu|int|mil|gov|arpa|biz|aero|name|coop|info|pro|museum))$/i;
    if(re.test(value)) return [true,"",""];
    else {
        return [false,"The value Email isn't valid ",""];
    }
}

function isValidEmail2(value) {
    var re = /^\w+([\.-]?\w+)*@(((([a-z0-9]{2,})|([a-z0-9][-][a-z0-9]+))[\.][a-z0-9])|([a-z0-9]+[-]?))+[a-z0-9]+\.([a-z]{2}|(com|net|org|edu|int|mil|gov|arpa|biz|aero|name|coop|info|pro|museum))$/i;
    if(re.test(value))  return true;
    else {
        alert("Введен некорректный Email");
        return false;
    }
}

function recLinkExt(action) {
    recLink('Исходящие ссылки', action);
}
function recLink(category, action) {
    try {
        if(typeof _gat != 'undefined' ){
            var pageTracker=_gat._getTracker('UA-12658219-1');
            pageTracker._trackEvent(category, action);
        }
    }catch(err){}
}

/*
$(document).ready(function() {
    $("#accordion").accordion({
        collapsible: true,
        active: false,

        autoHeight: false
    });
    $("a[id=slot_btn]").click(function(){
        window.open($(this).attr('title'), '#', 'resizable=no,status=no,location=no,toolbar=no,menubar=no,fullscreen=no,scrollbars=no,dependent=no,width=640,height=480');
        return false;
    });


    $("#search1").autocomplete("/jq_methods.jsp?get_domains=true",{
        delay:1,
        matchSubset:1,
        matchContains:1,
        cacheLength:10,
        maxItemsToShow:10

    });

    var country;
    $("a.zoom2").fancybox({
        'zoomSpeedIn'		:	250,
        'zoomSpeedOut'		:	1
    });


    $("#params_combo img[title]").tooltip({
        tip: '#tooltip_d',
        effect: 'slide'
    }).dynamic( {
            bottom: {
                direction: 'down',
                bounce: true
            }
        });
    $("#params_combo2 img[title]").tooltip({
        tip: '#tooltip_d',
        effect: 'slide'
    }).dynamic( {
            bottom: {
                direction: 'down',
                bounce: true
            }
        });


    */
/*
     if(!ie78){
     $(".select_field").custSelectBox();
     }
     *//*

});
*/
