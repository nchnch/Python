function printFrame(width, height, src) {
    var wWidth = document.documentElement.clientWidth ? document.documentElement.clientWidth : document.body.clientWidth;
    var wHeight = document.documentElement.clientHeight ? document.documentElement.clientHeight : document.body.clientHeight;
    document.write("<iframe name='frameSlot' id='frameSlot' frameborder='0' class='slot' ");

    document.write("width='");
    if (width > 0) {
        document.write(width);
    } else {
        document.write("80%");
    }
    document.write("' ");

    document.write("height='");
    if (height > 0) {
        document.write(height);
    } else {
        document.write("480px");
    }
    document.write("' ");

    document.write(" src='" + src + "'></iframe>");
}

function setSlotVisiability(visibility) {
    document.getElementsByTagName('iframe')[0].style.visibility = visibility;
}

function vote(slotid, rating) {
    var http = createRequestObject();
    if( http ) {
        http.open('post', 'vote.jsp?slotid=' + slotid + '&rating=' + rating);
        http.send(null);
    } else {
        document.location = link;
    }

    var uls = document.getElementsByTagName('ul');
    var ulsLnt = uls.length;

    for(var i=0; i<ulsLnt; i++)
    {

        if(uls[i].className == 'voting')
        {

            var as = uls[i].getElementsByTagName('a');
            var asLnt = as.length;

            for(var j=0; j<asLnt; j++)
            {
                as[j].className = j + 1 == rating? 'cur': '';
            }

            if(ltIE7)
            {
                uls[i].onmouseover = function()
                {
                    this.className += ' phover'
                }

                uls[i].onmouseout = function()
                {
                    this.className = this.className.replace(/(^| )phover($| )/,'')
                }
            }
        }
    }
}

function fullScreen() {
    var frame = document.getElementsByName('frameSlot')[0];
    window.open(frame.src,"","scrolling=no","fullscreen=yes,");
    window.moveTo(0, 0);
    window.resizeTo(screen.availWidth, screen.availHeight);
}

function increaseFrameSize() {
    changeFrameSize(100, 1);
}

function decreaseFrameSize() {
    changeFrameSize(100, -1);
}

function changeFrameSize(delta, direction) {
    var frame = document.getElementsByName('frameSlot')[0];
    var offset = $("[name=frameSlot]").position();
    var maxWidth = $(".slot").width();
    var newWidth = frame.clientWidth + direction * delta;
    if (newWidth > 100 && newWidth < maxWidth) {
        var sizeDelta = newWidth / frame.clientWidth;
        frame.height = frame.clientHeight * sizeDelta;
        frame.width = newWidth;
        resizeCover(sizeDelta, offset);
    }
}

function createRequestObject() {
    try { return new XMLHttpRequest() }
    catch(e) {
        try { return new ActiveXObject('Msxml2.XMLHTTP') }
        catch(e) {
            try { return new ActiveXObject('Microsoft.XMLHTTP') }
            catch(e) { return null; }
        }
    }
}

function extCl(link){
    isClick=true;
    $.ajax({
        url: "jq_methods.jsp",
        data: "os="+$.client.os+"&browser="+$.client.browser+"&link="+link+"&click_external=true",
        async: true
    });
}

function adjustCover(index, left, top, width, height) {
    var cover = $("#cover_" + index);
    cover.width(width);
    cover.height(height);
    var offset = $("[name=frameSlot]").position();
    cover.css({ left: offset.left + left, top: offset.top + top });
}

function resizeCover(delta, oldOffset) {
    var $covers = $(".cover");
    $covers.each(this, function(){
        if (cover.width() > 0) {
            var width = cover.width();
            cover.width(width * delta);
            var height = cover.height();
            cover.height(height*delta);

            var frameOffset = $("[name=frameSlot]").position();
            var offset = $(".cover").position();
            var left = offset.left - oldOffset.left + frameOffset.left;
            left = frameOffset.left + (left - frameOffset.left) * delta;
            var top = offset.top - oldOffset.top + frameOffset.top;
            top = frameOffset.top + (top - frameOffset.top) * delta;
            cover.css({ left: left, top: top });
        }
    });
}
