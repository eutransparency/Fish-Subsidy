from django.contrib.contenttypes.models import ContentType
from django.template import Library, Node
from listmaker.models import List

register = Library()

def latest_lists(number=5):
  return {
    'lists' : List.objects.all().order_by('-pk')[:5],
  }
register.inclusion_tag('blocks/latest_lists.html')(latest_lists)


@register.inclusion_tag('blocks/add_remove_item.html', takes_context=True)
def list_item_edit(context, list_object):
    ct = ContentType.objects.get_for_model(list_object)
    in_list = list_object in [i.content_object 
                            for i in context['request'].session['list_items']]
    
    return {
    'ct' : ct,
    'list_object' : list_object,
    'in_list' : in_list,
    }