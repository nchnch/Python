function loadByPost(link,target) {
    if (target == 'undefined') {
        target = '_top';
    }
    var text = '<form method="post" name="game" action="' + link + '&mode=FUN" target="' + target + '"><input value="0.10" type="hidden" name="min"/></form>';
    document.getElementById("extraDiv").innerHTML=text;
    document.forms.game.submit();
}

function openSlot(link,target) {
    if (link.match("^post:")) {
        link = link.substr(5, link.length - 1);
        loadByPost(link,target);
    } else {
        window.open(link);
    }
}