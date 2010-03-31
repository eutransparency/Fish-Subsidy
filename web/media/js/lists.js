$(function() {

    $('.list_form').each(function (i, el){
        $(el).children().hide();
        action = $(el).children('.action').attr('name');
        $(el).append('<a class="list_item list_'+action+'"><span></span></a>');
    });


    function update_list(obj) {
        $('.list_items').html('')
        new_list = $('<ul />')
        console.debug(obj)
        for (ikey in obj.items) {
            new_item = $('<li>tet</li>')
            new_item.html('<strong>'+obj.items[ikey].name+'</strong>')
            new_list.append(new_item)
            // console.debug(ikey)
            // console.debug(obj.items[ikey].name)
        }
        $('.list_items').html(new_list)
    }

    $('.list_item').click(function(){  
        item = $(this)
        object_id = $(this).parent().children('.object_id').attr('value');
        content_type = $(this).parent().children('.content_type').attr('value');
        action = $(this).parent().children('.action').attr('name');
        form_action = $(this).parent().attr('action');

        form_data = {
            content_type : content_type,
            object_id : object_id,
            action : action,
        }

        $.ajax({
            type: 'POST',
            url: form_action,
            data: form_data,
            success: function(obj){
                obj = eval('('+obj+')')
                update_list(obj)
                // alert(obj.action)
                if (obj.action == "add") {
                    item.removeClass('list_add')
                    item.addClass('list_remove')
                    item.parent().children('.action').attr('name', 'remove');
                }
                if (obj.action == "remove") {
                    item.removeClass('list_remove')
                    item.addClass('list_add')
                    item.parent().children('.action').attr('name', 'add');
                }
            },
        });

    });


});