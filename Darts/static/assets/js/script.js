function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function DeleteItem(owner, url)
{
    if(!confirm("Are you sure?"))
        return;

    $.post(url,
    {
        "csrfmiddlewaretoken": getCookie('csrftoken')
    },
    function()
    {
        var parent = owner.parentNode;
        $(parent).fadeOut(300, function(){$(this).remove();});
    },
    "json");
}

function setPopup(class_name, message)
{
    var delay = 3000;
    var fade_time = 400;
    var popup = $('#popup');
    popup.attr('class', 'alert ' + class_name)
            .html(message)
            .fadeIn(fade_time).delay(delay).fadeOut(fade_time);
}