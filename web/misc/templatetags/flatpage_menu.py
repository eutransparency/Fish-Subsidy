from django.template import Library, Node
from django.contrib.flatpages.models import FlatPage
register = Library()

def flatpage_menu():
    # Create an unordered list of all flatpages
    pages = FlatPage.objects.all()
    menu = '<ul>'
    for i in range(len(pages)):
        menu += '<li>'+'<a href="'+pages[i].url+'" title="'+pages[i].title+'">'+pages[i].title+'</a></li>'
    menu += '</ul>'
    return menu 

register.simple_tag(flatpage_menu)
