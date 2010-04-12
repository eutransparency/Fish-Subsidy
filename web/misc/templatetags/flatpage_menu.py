from django.template import Library, Node
from django.conf import settings
from multilingual.flatpages.models import MultilingualFlatPage
register = Library()

def flatpage_menu(language=settings.LANGUAGE_CODE):
    # Create an unordered list of all flatpages
    pages = MultilingualFlatPage.objects.all().for_language(language)

    menu = '<ul>'
    for page in pages:
        menu += '<li>'+'<a href="'+page.url+'" title="'+page.title+'">'+page.title+'</a></li>'
    menu += '</ul>'
    return menu 

register.simple_tag(flatpage_menu)
