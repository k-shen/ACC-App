$(document).ready(function() {
    $('.finish_zone').hide();
    $('img').one("click", function(e) {
        var offset = $(this).offset();
        var X = (e.pageX - offset.left);
        var Y = (e.pageY - offset.top);
        $('#coord').text('X: ' + X + ', Y: ' + Y);
        
        $('img').one("click", function(e) {
            var offset = $(this).offset();
            var X2 = (e.pageX - offset.left);
            var Y2 = (e.pageY - offset.top);
            $('#coord2').text('X2: ' + X2 + ', Y2: ' + Y2);
            
            var coords = [
                {
                    'bottomrightX': X2,
                    'bottomrightY': Y2,
                    'topleftX': X,
                    'topleftY': Y,
                }
            ]
            var cid = $('.finish_zone').attr('cid');
            var zid = $('.finish_zone').attr('zid');
            $('.finish_zone').show();
            document.getElementById("tlx").value = X;
            document.getElementById("tly").value = Y;
            document.getElementById("brx").value = X2;
            document.getElementById("bry").value = Y2;
        });
    });
});