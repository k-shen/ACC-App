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
});