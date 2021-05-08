from builtins import object
import logging

from bs4 import BeautifulSoup
from ckantoolkit.tests import factories
import pytest


log = logging.getLogger(__name__)


@pytest.mark.usefixtures('clean_db', 'clean_index')
class TestUIData(object):

    def create_datasets(self):
        organization = factories.Organization()
        self.group1 = factories.Group()
        self.group2 = factories.Group()
        self.dataset1 = factories.Dataset(owner_org=organization['id'], groups=[{"name": self.group1["name"]}])
        self.dataset2 = factories.Dataset(owner_org=organization['id'], groups=[{"name": self.group2["name"]}])
        sysadmin = factories.Sysadmin(name='testUpdate')
        self.user_name = sysadmin['name'].encode('ascii')

    def test_not_empty_sections(self, app):

        self.create_datasets()

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

    def test_api_doc_link(self, app):
        """Assert CKAN major/minor version matches API docs URL."""
        # TODO mock helpers.api_doc_url and then assert the mock was called
        # after the request. Is this possible in CKAN?
        from ckan.lib.helpers import ckan_version
        expected_version = '.'.join(ckan_version().split('.')[0:2])

        index_response = app.get('/dataset')
        html = BeautifulSoup(index_response.unicode_body, 'html.parser')

        # Test link to api docs matches CKAN version
        api_doc_href = html.find('a', string='API Docs')['href']
        assert expected_version in api_doc_href

    def test_api_url(self, app):
        """Assert API link on dataset page."""
        index_response = app.get('/dataset')

        html = BeautifulSoup(index_response.unicode_body, 'html.parser')
        api_href = html.find('a', string='API')['href']
        assert '/api/3' == api_href
