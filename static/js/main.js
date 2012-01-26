function processKeyPress(event) {
    if (event.keyCode=='13') selit();
}

function selit() {
    debugger;
    if(selVal==0)selVal=1;
    //alert($("#search"+selVal).val());
    window.location="search.jsp?query_string="+$("#search"+selVal).val()+"&search_type="+selVal;
}

function onVoteClick() {
    $.ajax({
        url:'/dataLoader?action=vote&id='+ $('input[name=vote_answer]').attr('id'),
        async: false,
        success: function(data, result) {
            if (!result)
                alert('Не удалось сохранить Ваш выбор :(');
        }});

    $.cookie('vote_id_'+$('input[name=vote_id]').val(), $('input[name=vote_id]').val(), {expires: 365});
    showResult();
}
$(function () {
    $('input[name=voteOk]', this).attr('disabled', 'disabled');

    var name = 'vote_id_'+$('input[name=vote_id]').val();
    if ($.cookie(name)) {
        showResult();
    }
    $('input[name=voteOk]', this).attr('disabled', 'disabled');
    $('input[name=vote_answer]').change(function() {
        $('input[name=voteOk]').removeAttr('disabled');
    });
});

function showResult() {
    var text = $.ajax({
        url:'/dataLoader?action=list&type=votes&vid=' + $('input[name=vote_id]').val(),
        async: false,
        success: function(data, result) {
            if (!result)
                alert('Ошибка сервера');
        }}).responseText;
    text += "<p class='align-right'><a href='/votes.jsp'>Ещё опросы...</a></p>";
    $('div[id=vote]').fadeOut('slow');
    $('div[id=vote]').html(text);
    $('div[id=vote]').fadeIn('slow');
}

// Function from index page
function extCl(link){
    $.ajax({
        url: "/jq_methods.jsp",
        data: "os="+$.client.os+"&browser="+$.client.browser+"&link="+link+"&click_external=true",
        async: true
    });
}
