from bs4 import BeautifulSoup
import logging
import json
from nose.tools import assert_equal, assert_in
import urllib2
from ckan import plugins as p
try:
    from ckan.tests.helpers import reset_db, FunctionalTestBase
    from ckan.tests import factories
except ImportError:
    from ckan.new_tests.helpers import reset_db, FunctionalTestBase
    from ckan.new_tests import factories

if p.toolkit.check_ckan_version(max_version='2.3'):
    from pylons import config
else:
    from ckan.plugins.toolkit import config

log = logging.getLogger(__name__)


class TestUIData(FunctionalTestBase):

    @classmethod
    def setup(cls):
        super(TestUIData, cls).setup_class()
        reset_db()
        
    def create_datasets(self):
        organization = factories.Organization()
        self.group1 = factories.Group()
        self.group2 = factories.Group()
        self.dataset1 = factories.Dataset(owner_org=organization['id'], groups=[{"name": self.group1["name"]}])
        self.dataset2 = factories.Dataset(owner_org=organization['id'], groups=[{"name": self.group2["name"]}])
        sysadmin = factories.Sysadmin(name='testUpdate')
        self.user_name = sysadmin['name'].encode('ascii')
       
    def test_not_empty_sections(self):
        
        self.create_datasets()
        
        app = self._get_test_app()
        index_response = app.get('/dataset')
        
        html = BeautifulSoup(index_response.unicode_body, 'html.parser')

        # get the main section where filters are included
        filters = html.find('div', attrs={'class': 'filters'})
        log.info('FILTERS: {}'.format(filters))

        # we expect "groups", "tags" and "organization"
        
        uls = filters.find_all('ul', attrs={"name": "facet"})
        assert len(uls) > 0
        for ul in uls:
            lis = ul.find_all('li', attrs={"class": "nav-item"})
            log.info('UL found {}. Elements: {}'.format(ul['id'], len(lis)))
            assert len(lis) > 0
            for li in lis:
                log.info('Elements found: {}'.format(li))
    
    def test_links(self):
        
        app = self._get_test_app()
        index_response = app.get('/dataset')
        
        html = BeautifulSoup(index_response.unicode_body, 'html.parser')

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        # Test link to api docs in CKAN 2.8
        element = html.find('a', string='API Docs')
        log.info('Test URL: {}'.format(element['href']))
        assert_in('2.8', element['href'])
        req = urllib2.Request(element['href'], headers=headers)
        result = urllib2.urlopen(req)
        assert_equal(200, result.getcode())
        
        # Test API URL
        element = html.find('a', string='API')
        if element['href'].startswith('/'):
            element['href'] = config['ckan.site_url'] + element['href']
        log.info('Test URL: {}'.format(element['href']))
        req = urllib2.Request(element['href'], headers=headers)
        result = urllib2.urlopen(req)
        assert_equal(200, result.getcode())
        