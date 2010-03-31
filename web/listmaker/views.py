from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import json
import models
import forms
from django.contrib.auth.decorators import login_required


@login_required
def manage_lists(request, list_id=None):
    if list_id:
        list_item = get_object_or_404(models.List, pk=list_id, user=request.user)
    else:
        list_item = models.List(user=request.user)
    
    if request.POST:
        new_list_form = forms.ListForm(request.POST, instance=list_item)
        new_list_form.user = request.user
        if new_list_form.is_valid():
            new_list_form.save()
        
    else:
        new_list_form = forms.ListForm(instance=list_item)
    return render_to_response(
        'edit.html', 
            {
                'new_list_form': new_list_form, 
            }, context_instance = RequestContext(request))
            
@login_required
def my_lists(request):
    lists = models.List.objects.filter(user=request.user)
    return render_to_response(
        'mylists.html',
            {
                'lists': lists,
            }, context_instance = RequestContext(request))


def list_view(request, list_id):
    try:
        list_item = models.List.objects.select_related().get(pk=list_id)
    except models.List.DoesNotExist:
        raise Http404


    # list_item = models.List.objects.select_related().get(pk=4)

    return render_to_response(
        'list_item.html',
            {
                'list_item': list_item,
            }, context_instance = RequestContext(request))


def edit_list_items(request, list_id=None):
    if list_id:
        try:
            list_object = models.List.objects.get(pk=list_id)
            request.session['list_object'] = list_object
            
        except models.List.DoesNotExist:
            return HttpResponseRedirect(reverse('create_list'))
    request.session['list_enabled'] = True
    list_items = [i for i in list_object.listitem_set.all()]
    request.session['list_items'] = list_items
    list_total = [i.content_object.amount for i in list_items]
    request.session['list_total'] = list_total
    
    request.session.modified = True
    return HttpResponseRedirect(reverse('list_detail', args=(list_object.pk,)))


def add_remove_item(request):
    """
    Expects POST data with the following values:
        * content_type
        * object_id
        
    Only contnet types with a valid `LIST_ENABLED` attribute will be allowed
    """
    # Validataion
    if not request.POST:
        return HttpResponse(
            json.dumps({
                'type' : 'error',
                'message' : 'Invalid request (Expected POST data)'}
                ),
            status=200)
    
    if not request.session.get('list_enabled'):
        return HttpResponse(
            json.dumps({
                'type' : 'error',
                'message' : 'No List'}
                ),
            status=200)
    list_object = request.session.get('list_object')
    content_type = request.POST.get('content_type')
    object_id = request.POST.get('object_id')
            
    if not content_type or not object_id:
        content = {
            'type' : 'error',
            'message' : 'content_type and or object_id not specified'
        }
        res = HttpResponse(json.dumps(content), status=500)
        return res    
    try:
        ct = ContentType.objects.get(name=content_type)
    except:
        return HttpResponse(json.dumps({'type' : 'error', 'message' : 'invalid content type'}), status=500)

    try:
        co = ct.get_object_for_this_type(pk=object_id)
    except:
        return HttpResponse(json.dumps({'type' : 'error', 'message' : 'invalid object id'}), status=500)

    # Load the current list
    list_items = request.session['list_items']
    
    # Load the object we're adding or removing
    list_object = models.List.objects.get(pk=4)
    list_item = models.ListItem(list_id=list_object, content_object=co)
    print co
    action = request.POST.get('action')

    # print dir(request.session['list_items'])
    # print request.session['list_items'].index(list_item)
    # print list_item
    
    if action == "add":
        # print list_item in request.session['list_items']
        if list_item.content_object not in [i.content_object for i in list_items]:
            print 'added'
            list_items.append(list_item)

    if action == "remove":
        try:
            list_items.remove(list_item)
            print 'removed'            
        except:
            pass
    # Create the total for this list
    list_total = sum([i.content_object.amount for i in list_items])
    
    
    # Remake the session items
    request.session['list_total'] = list_total
    request.session['list_items'] = list_items
    
    # We'll need a dict of the items.
    # TODO: one day this should get all the attributes from the model, so we
    # don't hard code any fields.
    items_dict = {}
    for i in list_items:
        co = i.content_object
        items_dict[co.pk] = co.__dict__
    
    # Do this to make sure the list is always updated
    request.session.modified = True
    if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        return HttpResponse(json.dumps(
            {
            'message' : 'invalid object id',
            'total' : list_total,
            'action' : action,
            'items' : items_dict
            }))
        
    res = HttpResponseRedirect(request.META['HTTP_REFERER'])
    return res
        