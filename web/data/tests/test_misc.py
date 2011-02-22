"""
Tests various functions, like context processors.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse

class MiscTest(TestCase):


    def test_header_class_valid(self):
        view = reverse('home',)
        response = self.client.get(view)
        valid = True
        try:
            response.context['header_class']
        except:
            valid = False
        self.assertEqual(valid, True)
    
