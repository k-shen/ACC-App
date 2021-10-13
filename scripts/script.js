$(document).ready(function() {
    $('.delete-cam-button').on('click',function(){
        var name = $(this).parent().attr('name');
        console.log(name);
        if (confirm('Are you sure you want to delete this camera angle ('+name+')?')){
            var cid = $(this).attr('cid');
            $.ajax({
                method: "POST",
                url: "/cam/"+cid+"/delete",
                data: {cid: cid}
            });
            window.location.href = '/home';
        }
    });
    $('.view-cam-button').on('click',function(){
        var name = $(this).parent().attr('name');
        var cid = $(this).attr('cid');
        window.location.href = '/cam/'+cid;
    });

    $('.delete-vid-button').on('click',function(){
        var name = $(this).parent().attr('name');
        var cid = $(this).parent().parent().attr('cid');
        if (confirm('Are you sure you want to delete this video ('+name+')?')){
            var vid = $(this).attr('vid');
            $(this).parent().remove();
            $.ajax({
                method: "POST",
                url: "/vid/"+vid+"/delete",
                data: {
                    vid: vid,
                    cid: cid,
                }
            });
        }
    });
    $('.delete-zone-button').on('click',function(){
        var name = $(this).parent().attr('name');
        var cid = $(this).parent().parent().attr('cid');
        if (confirm('Are you sure you want to delete this zone ('+name+')?')){
            var zid = $(this).attr('zid');
            $(this).parent().remove();
            $.ajax({
                method: "POST",
                url: "/zone/"+zid+"/delete",
                data: {
                    zid: zid,
                    cid: cid,
                }
            });
        }
    });
    $('#switchVZ').on('click', function() {
        if (document.getElementById('vid_table').style.display == 'none') {
            document.getElementById('vid_table').style.display = '';
            document.getElementById('zone_table').style.display = 'none';
            $(this).text('Zones');
        } else {
            document.getElementById('vid_table').style.display = 'none';
            document.getElementById('zone_table').style.display = '';
            $(this).text('Video');
        }
    });

    $("#adding").on('click', function() {
        var cid = $(this).attr("cid")
        console.log(cid)
        if (document.getElementById('vid_table').style.display == 'none') {
            $('#adding').attr('action', "/cam/"+cid+"/addZone").submit();
        } else {
            $('#adding').attr('action', "/cam/"+cid+"/addVideo").submit();
        }
    })
});