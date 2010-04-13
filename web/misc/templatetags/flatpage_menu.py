from django.template import Library, Node
from django.conf import settings
from multilingual.flatpages.models import MultilingualFlatPage
register = Library()

def flatpage_menu(language=settings.LANGUAGE_CODE):
    # Create an unordered list of all flatpages
    pages = MultilingualFlatPage.objects.all().for_language(language)

    menu = '<ul>'
    for page in pages:
        menu += """
        <li><a href="%(url)s" title="%(title)s">%(title)s</a></li>
        """ % {
            'url' : page.url or "",
            'title' : page.title or "",
        }
    menu += '</ul>'
    return menu 

register.simple_tag(flatpage_menu)
