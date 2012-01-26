var currentId = 0;

function openDialog(callback, logoId) {
    var cancel = function() {
        $("#browseImageDialog").dialog("close");
    };
    var getResponse = function(){
        callback();
        $("#browseImageDialog").dialog("close");
    };

    var dialogOpts = {
        modal: true,
        width: 1080,
        height:760,
        buttons: {
            "ОК": getResponse,
            "Отмена": cancel
        },
        autoOpen: false,
        open: function() {
            //load types select
            $.getJSON("/imageBrowser?action=types", function(data) {
                $("#types option").remove();
                var options = $("#types");
                $.each(data, function() {
                    options.append($("<option />").val(this.id).text(this.name));
                });

                refreshImages();
            });
        }
    };
    $("#browseImageDialog").dialog(dialogOpts);

    $.getJSON('/imageBrowser?action=get&imgId=' + logoId, function(data){
        if (data != "undefined" && data != "") {
            $("#current").attr('src', data.fileName);
        } else {
            $("#current").attr('src', '/images/logos/no_logo.jpg');
        }
    });

    $("#browseImageDialog").dialog("open");
}

function refreshImages() {
    var page = $("#page").val();
    var type = $("#types").val();
    var showBy = $("#showBy").val();

    $.getJSON('/imageBrowser?action=list&userId=0&type=' + type + '&page=' + page + '&showBy=' + showBy, function(data){
        if (data != "undefined" && data != "") {
            var entries = data.entities;

            //insert data
            var text = "<table>";
            var row = 0;
            $.each(entries, function() {
                var Entry = this;
                if (row % 5 == 0 && row > 0) {
                    text += "</tr><tr>";
                }
                text += '<td><a href="#" onclick="setImage(' + Entry.id + ');"><img id="img_' + Entry.id + '" src="' + Entry.fileName + '" alt="' + Entry.name + '" width="200"/></a></td>';
                row++;
            });
            text += "</tr></table>"
            $("#images").html(text);

            //paging
            $("#page").val(data.page);
            text = "";
            for (var i = 1; i <= data.totalPage; i++) {
                if (i == data.page) {
                    text += "<label>" + i + "</label>";
                } else {
                    text += "<a href='#' onclick='$(\"#page\").val(" + i + "); refreshImages();' >" + i + "</div>";
                }
                text += "&nbsp;";
            }
            $("#pages").html(text);
        } else {
            var text = "<div>Нет загруженных картинок</div>";
            $("#images").html(text);
            $("#pages").html('');
        }
    });
}

function setImage(id) {
    var src = $("#img_" + id).attr('src');
    $("#current").attr('src', src);
    currentId = id;
}

function uploadFile(type){
    $.ajaxFileUpload({
        url:'/imageBrowser?type=' + type + '&userId=0', //casino logo
        secureuri:false,
        fileElementId:'fileToUpload',
        dataType: 'json',
        success: function (data, status) {
            $("#current").attr('src', data.fileName);
            currentId = data.id;
        },
        error: function (data, status, e)
        {
            alert(e);
        }
    });
    return false;
}

function getCurrentImage() {
    return $("#current").attr('src');
}

function getCurrentImageId() {
    return currentId;
}