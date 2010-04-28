$(function() {

    $(".list_block").wrap('<div class="lists_footer" />')
    $('.lists_footer').remove().insertAfter('#footer')    
    $('.lists_footer .list_block h3').click(function() {
        $('.lists_footer .list_block .list_items').toggle()
    });
    $('.lists_footer .list_block').resizable({ handles: 'n, e, s, w' })
    
    
    function make_icons(){
        $('.list_form').each(function (i, el){
            alerady_converted = $(el).children('.list_item');
            if ($(alerady_converted).length == 0) {
                $(el).children().hide();
                action = $(el).children('.action').attr('name');                
                $(el).append('<a class="list_item list_'+action+'"><span></span></a>');                
            }
        });
    }

    make_icons()
    
    function update_list(obj) {
        $('.list_items').html(obj.html)
        console.debug(obj.html)
        // $('.list_items').html("eret")
        make_icons()
    }
    
    function animate_add(obj) {
        $(obj).parent().parent().parent().parent().effect('transfer', { to: $(".lists_footer") }, 10000)
    }

    $('.list_item').live('click', function(){  
        item = $(this)
        object_id = $(this).parent().children('.object_id').attr('value');
        content_type = $(this).parent().children('.content_type').attr('value');
        list_item_id = $(this).parent().children('.list_item_id').attr('value');
        action = $(this).parent().children('.action').attr('name');
        form_action = $(this).parent().attr('action');
        animate_add(this)
        form_data = {
            content_type : content_type,
            object_id : object_id,
            list_item_id : list_item_id,
            action : action,
        }

        $.ajax({
            type: 'POST',
            url: form_action,
            data: form_data,
            success: function(obj){
                console.debug(obj)
                obj = eval('('+obj+')')
                update_list(obj)
                item = $("[value="+obj.list_item_id+"]").parent().children('.list_item')
                if (obj.action == "add") {
                    item.each(function(i, el) {
                        el = $(el)
                        el.removeClass('list_add')
                        el.addClass('list_remove')
                        el.parent().children('.action').attr('name', 'remove');                        
                    })
                }
                if (obj.action == "remove") {
                    item.each(function(i, el) {
                        el = $(el)                        
                        el.removeClass('list_remove')
                        el.addClass('list_add')
                        el.parent().children('.action').attr('name', 'add');
                    })
                }
            },
        });

    });


});