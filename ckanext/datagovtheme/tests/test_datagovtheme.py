# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
import ckanext.harvest.model as harvest_model
from ckan.tests import factories
from ckan.tests.helpers import reset_db
from ckan.lib.helpers import url_for
from ckan.lib.search import rebuild
import pytest
import re


# The /dataset page uses get_pkg_dict_extra which depends on HarvestObject,
# hence the harvest extension. Include it for these tests.
@pytest.mark.ckan_config('ckan.plugins', 'harvest geodatagov datagovtheme spatial_metadata')
@pytest.mark.use_fixtures('with_plugins', 'clean_db')
class TestDatagovthemeServed(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    @classmethod
    def setup_class(cls):
        # Start data json sources server we can test harvesting against it
        harvest_model.setup()

    @classmethod
    def setup_method(self):
        reset_db()
        rebuild()

    def get_base_dataset(self):
        self.user = factories.Sysadmin()
        self.user_name = self.user['name'].encode('ascii')
        self.organization = factories.Organization(name='myorg',
                                                   users=[{'name': self.user_name, 'capacity': 'Admin'}],
                                                   extras=[{'key': 'sub-agencies', 'value': 'sub-agency1,sub-agency2'}])
        dataset = {
            'public_access_level': 'public',
            'unique_id': '',
            'owner_org': self.organization['id'],
            'extras': []
        }
        return dataset

    def create_datasets(self, dataset):
        d1 = dataset.copy()
        d1.update({'title': 'test 01 dataset', 'unique_id': 't1'})
        new_dataset = factories.Dataset(**d1)
        return new_dataset['id']

    def test_homepage_redirect(self, app):
        index_response = app.get('/')

        assert 'Welcome to Geospatial Data' not in index_response.body
        assert 'datasets found' in index_response.body

    def test_datagovtheme_css_file(self, app):
        """Assert the correct version of CSS is served."""
        index_response = app.get('/dataset')

        # Note: in development/debug mode, this asset uses the output filename
        # in webassets.yml. In production mode, it is compiled to a different
        # name and may have addtional filters (e.g. minification) applied.
        assert 'datagovtheme.css' in index_response.body

    def test_datagovtheme_html_loads(self, app):
        index_response = app.get('/dataset')

        assert "An official website of the United States government" in index_response.body
        assert "Search datasets..." in index_response.body
        assert "datasets found" in index_response.body

    def test_datagovtheme_navigation(self, app):
        index_response = app.get('/dataset')

        assert '<span class="text-uppercase">Data</span></a>' in index_response.body
        assert '<span class="text-uppercase">Reports</span></a>' in index_response.body
        assert '<span class="text-uppercase">Open Government</span></a>' in index_response.body
        assert '<span class="text-uppercase">Contact</span></a>' in index_response.body
        assert '<span class="text-uppercase">User Guide</span></a>' in index_response.body

    def test_datagovtheme_organizations(self, app):
        self.create_datasets(self.get_base_dataset())

        index_response = app.get('/organization')

        org_match = r'1 organizations? found'
        matches = re.findall(org_match, index_response.body)
        assert len(matches) > 0
        assert "Search organizations..." in index_response.body
        assert "What are organizations?" in index_response.body

    def test_datagovtheme_bureau_names(self, app):
        dataset = self.get_base_dataset()
        dataset['extras'].append({'key': 'bureauCode', 'value': '010:00'})
        self.create_datasets(dataset)

        index_response = app.get('/dataset')

        assert "<a href=\"/dataset/?bureauCode=010%3A00\" title=\"\">" in index_response.body
        assert "<span class=\"item-label\">Department of the Interior</span>" in index_response.body

    def test_datagovtheme_package_metadata(self, app):
        dataset = self.get_base_dataset()
        dataset['extras'].append({'key': 'contact-email', 'value': 'test@email.com'})
        dataset_id = self.create_datasets(dataset)

        index_response = app.get(url_for("dataset.read", id=dataset_id), status=200)

        assert '<a href=mailto:test@email.com>test@email.com</a>' in index_response.body
