setInterval(function() {
    date = new Date(),
    $("#time").html(date.toUTCString());
}, 1000);