function alertFunc() {
    $.ajax({
        url: "/static/test.txt",
        dataType: "text",
        success: function (data) {
            console.log(data);
            $("#div1").text(data);
        }
    });
}




