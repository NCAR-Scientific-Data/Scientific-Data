$(function () {
    $("#go").click(function () {
        var text = $("#text").val();
        $.getJSON("myservice?text=" + encodeURIComponent(text), function (data) {
            $("#output").text(data.reversed);
        });
    });
});
