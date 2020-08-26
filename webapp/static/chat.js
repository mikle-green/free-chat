setInterval(function() {
    var chat_data = $("#chat").html();
    var msg_count_data = (chat_data) ? $("#msg_count").html() : "0";
    $.ajax({
        url: "/chat",
        data: "msg_count=" + msg_count_data,
        dataType: "html",
        statusCode: {
            200: function(response) {
                $("#chat").html(response);
            },
        },
    });
}, 1000);

var submit_with_reset = function(event) {
    $(".container").off("submit", "#contact", submit_with_reset);
    $(this).trigger(event);
    $("#message").val("");
    $("#send").blur();
    $(".container").on("submit", "#contact", submit_with_reset);
    return false;
};

$(".container").on("submit", "#contact", submit_with_reset);

$(function() {
    element = $("#chat")
    element.scrollTop(element.prop("scrollHeight"));
});