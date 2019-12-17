if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) { // mobile
    $(".tips-right").hide()
    $(".tips-msg").hide()
} else { // PC
    var $msg1 = $('.msg1')
    $('.msg1 .erweima').qrcode(window.location.href);

    $(".tip1").hover(function() {
        $msg1.show()
    }, function() {
        $msg1.hide()
    })

    var $msg2 = $('.msg2')
    $(".tip2").hover(function() {
        $msg2.show()
    }, function() {
        $msg2.hide()
    })
}

