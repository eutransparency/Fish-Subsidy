from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from models import RecipientComment

def all_annotations(request):
    
    annotations = RecipientComment.objects.all()
    
    return render_to_response(
        'all_annotations.html', 
        {
            'annotations' : annotations,
        },
        context_instance=RequestContext(request)
        )