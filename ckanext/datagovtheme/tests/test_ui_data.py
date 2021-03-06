from builtins import object

from bs4 import BeautifulSoup
from ckantoolkit.tests import factories
import pytest


# The /dataset page uses get_pkg_dict_extra which depends on HarvestObject,
# hence the harvest extension. Include it for these tests.
@pytest.mark.ckan_config('ckan.plugins', 'harvest datagovtheme')
@pytest.mark.use_fixtures('with_plugins', 'clean_db', 'clean_index')
class TestSearchFilters():

    @pytest.fixture(autouse=True)
    def set_up(self):
        organization = factories.Organization()
        self.group1 = factories.Group()
        self.group2 = factories.Group()
        self.dataset1 = factories.Dataset(owner_org=organization['id'], groups=[{"name": self.group1["name"]}])
        self.dataset2 = factories.Dataset(owner_org=organization['id'], groups=[{"name": self.group2["name"]}])

    def test_not_empty_sections(self, app):
        index_response = app.get('/dataset')

        html = BeautifulSoup(index_response.body, 'html.parser')

        # get the main section where filters are included
        filters = html.select_one('div.filters')
        assert filters, "Could not find div.filters"

        # Get the section "names"
        filter_names = [' '.join(filter_header.stripped_strings)
                        for filter_header in filters.select('section.module .module-heading')]
        assert len(filter_names) > 0, "Could not find section.module .module-heading"

        assert 'Organizations' in filter_names
        assert 'Tags' in filter_names
        assert 'Bureaus' in filter_names
        assert 'Publishers' in filter_names


class TestApiLinks(object):
    def test_api_doc_link(self, app):
        """Assert CKAN major/minor version matches API docs URL."""
        # TODO mock helpers.api_doc_url and then assert the mock was called
        # after the request. Is this possible in CKAN?
        from ckan.lib.helpers import ckan_version
        expected_version = '.'.join(ckan_version().split('.')[0:2])

        index_response = app.get('/dataset')
        html = BeautifulSoup(index_response.body, 'html.parser')

        # Test link to api docs matches CKAN version
        api_doc_href = html.find('a', string='API Docs')['href']
        assert expected_version in api_doc_href

    def test_api_url(self, app):
        """Assert API link on dataset page."""
        index_response = app.get('/dataset')

        html = BeautifulSoup(index_response.body, 'html.parser')
        api_href = html.find('a', string='API')['href']
        assert '/api/3' == api_href
