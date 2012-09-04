import json

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count

from models import RecipientComment
from data.models import Port

def all_annotations(request):
    
    annotations = RecipientComment.objects.all()
    annotations_map = RecipientComment.objects.values('recipient__port', 'recipient__port__lat', 'recipient__port__lng').annotate(count=Count('recipient__port')).order_by('-count')
        
    return render_to_response(
        'all_annotations.html', 
        {
            'annotations' : annotations,
            'annotations_map' : annotations_map,
        },
        context_instance=RequestContext(request)
        )
def annotations_for_port(request, port_id):
    port = Port.objects.get(pk=port_id)
    comments_for_port = RecipientComment.objects.filter(recipient__port=port_id)
    return render_to_response(
        'ahah_comments.html', 
        {
            'comments_for_port' : comments_for_port,
            'port' : port,
        },
        context_instance=RequestContext(request)
        )
    