from django.test import TestCase
from django.core.urlresolvers import reverse
from data.models import Scheme
from decimal import *

class SchemesTest(TestCase):
    

    
    def test_top_schemes(self):
        """
        Top schemes across all years and all countries.
        """
        
        schemes = Scheme.objects.top_schemes(year=0)
        top_10 = [s.schemetotal for s in schemes]

        expected = [
                    Decimal('1383887143.79'), 
                    Decimal('1197392161.18'), 
                    Decimal('1043921789.05'), 
                    Decimal('560054775.11'), 
                    Decimal('458481641.47'), 
                    Decimal('443886256.81'), 
                    Decimal('409196537.55'), 
                    Decimal('348184825.78'), 
                    Decimal('347770118.96'), 
                    Decimal('343237386.34')]
        self.assertEqual(top_10, expected)
        

    def test_GB_top_schemes(self):
        """
        Top schemes across all years in GB.
        """

        self.maxDiff = None
        
        schemes = Scheme.objects.top_schemes(year=0, country='GB')
        top_10 = [s.schemetotal for s in schemes]
        expected = [
                    Decimal('119326075.91'),
                    Decimal('82651362.44'),
                    Decimal('37341488.85'),
                    Decimal('30789541.00'),
                    Decimal('28551704.87'),
                    Decimal('19300279.34'),
                    Decimal('17462875.22'),
                    Decimal('9940472.94'),
                    Decimal('8681613.78'),
                    Decimal('6820384.03') 
                    ]
        self.assertEqual(top_10, expected)
        

    def test_GB_schemes_2007(self):
        """
        Top schemes in the UK in 2007
        """

        self.maxDiff = None
        
        schemes = Scheme.objects.top_schemes(year=2007, country='GB')
        top_10 = [s.schemetotal for s in schemes]
        expected = [
                    Decimal('4503804.21'), 
                    Decimal('3620944.00'), 
                    Decimal('1772266.19'), 
                    Decimal('1241969.80'), 
                    Decimal('921974.06'), 
                    Decimal('334061.67'), 
                    Decimal('316596.92'), 
                    Decimal('192578.12'), 
                    Decimal('152614.00'), 
                    Decimal('23558.64')
                    ]
        
        self.assertEqual(top_10, expected)
        
