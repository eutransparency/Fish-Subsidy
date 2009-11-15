import sys
sys.path.append('../../../')
sys.path.append('/var/www/fishsubsidy/web')
from feeds import parse

import django
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    parse.parse()
