# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
import ckanext.harvest.model as harvest_model
from ckan.tests import factories
from ckan.tests.helpers import reset_db
import pytest
import re


# The /dataset page uses get_pkg_dict_extra which depends on HarvestObject,
# hence the harvest extension. Include it for these tests.
@pytest.mark.ckan_config('ckan.plugins', 'harvest datagovtheme')
@pytest.mark.use_fixtures('with_plugins', 'clean_db')
class TestDatagovthemeServed(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    @classmethod
    def setup(cls):
        # Start data json sources server we can test harvesting against it
        reset_db()
        harvest_model.setup()

    def create_datasets(self):
        self.user = factories.Sysadmin()
        self.user_name = self.user['name'].encode('ascii')
        self.organization = factories.Organization(name='myorg',
                                                   users=[{'name': self.user_name, 'capacity': 'Admin'}],
                                                   extras=[{'key': 'sub-agencies', 'value': 'sub-agency1,sub-agency2'}])
        dataset = {
            'public_access_level': 'public',
            'unique_id': '',
            'contact_name': 'Jhon',
            'contact_email': 'jhon@mail.com',
            'modified': '2019-01-27 11:41:21',
            'tag_string': 'tag01,tag02',
            'version': '1.1',
            'owner_org': self.organization['id'],
            'extras': [{'key': 'bureauCode', 'value': '010:00'}]
        }
        d1 = dataset.copy()
        d1.update({'title': 'test 01 dataset', 'unique_id': 't1'})
        factories.Dataset(**d1)

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

        assert "Search Data.Gov" in index_response.body
        assert "Search datasets..." in index_response.body
        assert "datasets found" in index_response.body

    def test_datagovtheme_navigation(self, app):
        index_response = app.get('/dataset')

        assert '<li class="active"><a href="/dataset">Data</a></li>' in index_response.body
        assert '<a class="dropdown-toggle" data-toggle="dropdown">Topics<b\n            class="caret"></b></a>' \
               in index_response.body
        assert '<li><a href="//resources.data.gov">Resources</a></li>' in index_response.body
        assert '<li><a href="//strategy.data.gov">Strategy</a></li>' in index_response.body
        assert '<li><a href="//www.data.gov/developers/">Developers</a></li>' in index_response.body
        assert '<li><a href="//www.data.gov/contact">Contact</a></li>' in index_response.body

    def test_datagovtheme_topics(self, app):
        index_response = app.get('/dataset')

        assert '<li class="menu-agriculture">' in index_response.body
        assert '<li class="menu-climate">' in index_response.body
        assert '<li class="menu-energy">' in index_response.body
        assert '<li class="menu-local-government">' in index_response.body
        assert '<li class="menu-maritime">' in index_response.body
        assert '<li class="menu-ocean">' in index_response.body
        assert '<li class="menu-older-adults-health">' in index_response.body

    def test_datagovtheme_organizations(self, app):
        # create datasets
        self.create_datasets()

        index_response = app.get('/organization')

        org_match = r'1 organizations? found'
        matches = re.findall(org_match, index_response.body)
        assert len(matches) > 0
        assert "Search organizations..." in index_response.body
        assert "What are organizations?" in index_response.body

    def test_datagovtheme_bureau_names(self, app):
        # create datasets
        self.create_datasets()

        index_response = app.get('/dataset')

        assert "<a href=\"/dataset/?bureauCode=010%3A00\" title=\"\">" in index_response.body
        assert "<span class=\"item-label\">Department of the Interior</span>" in index_response.body
