from django.test import TestCase
from django.core.urlresolvers import reverse

class ViewsTest(TestCase):

    def viewtester(self, view, code=200):
        response = self.client.get(view)
        self.assertEqual(response.status_code, code)


    def test_home(self):
        view = reverse('home',)
        self.viewtester(view)
    
    def test_country(self):
        view = reverse('country', kwargs={'country': 'EU'})
        self.viewtester(view)
    
    def test_scheme_page(self):
        view = reverse('schemes', kwargs={'country': 'EU', })
        self.viewtester(view)
    
    def test_tuna_fleet(self):
        view = reverse('tuna_fleet', kwargs={'country': 'EU', })
        self.viewtester(view)

    def test_infringements(self):
        view = reverse('infringements')
        self.viewtester(view)

    def test_browse_ports(self):
        view = reverse('browse_ports', kwargs={'country': 'EU', })
        self.viewtester(view)
    
        view = reverse('browse_ports', kwargs={'country': 'EU', 'year' : 2007 })
        self.viewtester(view)
    
    def test_port(self):
        view = reverse('port', kwargs={'country': 'EU', 'port' : 'LOWESTOFT'})
        self.viewtester(view)
    
        view = reverse('port', kwargs={'country': 'EU', 'port' : 'LOWESTOFT', 'year' : 2007})
        self.viewtester(view)

    def test_browse_geo1(self):
        view = reverse('browse_geo1', kwargs={'country': 'EU', })
        self.viewtester(view)

    def test_browse_geo2(self):
        view = reverse('browse_geo2', kwargs={'country': 'EU', 'geo1' : 'Galicia'})
        self.viewtester(view)

    def test_nonvessel(self):
        view = reverse('nonvessel', kwargs={'country': 'EU', 'project_no' : '1173680019'})
        self.viewtester(view)

    def test_project_no(self):
        view = reverse('vessel', kwargs={'country': 'EU', 'cfr' : 'GBR000A17736', 'name' : 'thornella'})
        self.viewtester(view)


    