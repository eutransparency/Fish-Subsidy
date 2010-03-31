from django.conf.urls.defaults import *
import django.contrib.auth.views as auth_views

import views as list_views
import forms

urlpatterns = patterns('',
   url(r'^lists/edit/(?P<list_id>\d+)/$',list_views.manage_lists, name='edit_list'),
   url(r'^lists/create/$',list_views.manage_lists, name='create_list'),
   url(r'^lists/mylists$',list_views.my_lists,),
   url(r'^lists/(?P<list_id>\d+)/$',list_views.list_view, name="list_detail"),
   url(r'^lists/edit_items/(?P<list_id>\d+)/$',list_views.edit_list_items, name="edit_list_items"),
   
   # List Management stuff
   url(r'^lists/item/add/$',list_views.add_remove_item, name='list_item_add'),
   
   )