from bs4 import BeautifulSoup
import logging
from nose.tools import assert_equal, assert_in

try:
    from ckan.tests.helpers import FunctionalTestBase, reset_db
    from ckan.tests import factories
except ImportError:
    from ckan.new_tests.helpers import FunctionalTestBase, reset_db
    from ckan.new_tests import factories


log = logging.getLogger(__name__)


class TestUIData(FunctionalTestBase):

    def tearDown(self):
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

    def test_api_doc_link(self):
        """Assert CKAN major/minor version matches API docs URL."""
        # TODO mock helpers.api_doc_url and then assert the mock was called
        # after the request. Is this possible in CKAN?
        from ckan.lib.helpers import ckan_version
        expected_version = '.'.join(ckan_version().split('.')[0:2])

        app = self._get_test_app()
        index_response = app.get('/dataset')
        html = BeautifulSoup(index_response.unicode_body, 'html.parser')

        # Test link to api docs matches CKAN version
        api_doc_href = html.find('a', string='API Docs')['href']
        assert_in(expected_version, api_doc_href)

    def test_api_url(self):
        """Assert API link on dataset page."""
        app = self._get_test_app()
        index_response = app.get('/dataset')

        html = BeautifulSoup(index_response.unicode_body, 'html.parser')
        api_href = html.find('a', string='API')['href']
        assert_equal('/api/3', api_href)
