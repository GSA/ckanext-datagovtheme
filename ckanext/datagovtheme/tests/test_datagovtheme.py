# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
from ckantoolkit.tests.helpers import FunctionalTestBase
from nose.tools import assert_in, assert_true, assert_not_in, assert_false

from ckan import plugins as p
import mock
import ckanext


class TestDatagovthemeServed(FunctionalTestBase):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    @classmethod
    def setup_class(cls):
        super(TestDatagovthemeServed, cls).setup_class()

        if not p.plugin_loaded('geodatagov'):
            p.load('geodatagov')

        if not p.plugin_loaded('datagovtheme'):
            p.load('datagovtheme')

    @classmethod
    def teardown_class(cls):
        super(TestDatagovthemeServed, cls).teardown_class()
        p.unload('geodatagov')
        p.unload('datagovtheme')

    def test_plugin_loaded(self):
        assert_true(p.plugin_loaded('datagovtheme'))
        assert_true(p.plugin_loaded('geodatagov'))

    def test_datagovtheme_css_file(self):
        app = self._get_test_app()

        index_response = app.get('/dataset')
        
        if ckanext.datagovtheme.helpers.is_bootstrap2():
            assert_in('datagovtheme_bootstrap2.css', index_response.unicode_body)
            assert_not_in('datagovtheme.css', index_response.unicode_body) 
        else:
            assert_in('datagovtheme.css', index_response.unicode_body)
            assert_not_in('datagovtheme_bootstrap2.css', index_response.unicode_body)
    
    def test_datagovtheme_html_loads(self):
        app = self._get_test_app()

        index_response = app.get('/dataset')
    
        assert_in("Search Data.Gov", index_response.unicode_body)
        assert_in("Search datasets...", index_response.unicode_body)
        assert_in("No datasets found", index_response.unicode_body)

    def test_datagovtheme_navigation(self):
        app = self._get_test_app()

        index_response = app.get('/dataset')

        assert_in('<li class="active"><a href="/dataset">Data</a></li>', index_response.unicode_body)
        assert_in('<a class="dropdown-toggle" data-toggle="dropdown">Topics<b\n            class="caret"></b></a>', index_response.unicode_body)
        assert_in('<li><a href="//resources.data.gov/">Resources</a></li>', index_response.unicode_body)
        assert_in('<li><a href="//strategy.data.gov">Strategy</a></li>', index_response.unicode_body)
        assert_in('<li><a href="//www.data.gov/developers/">Developers</a></li>', index_response.unicode_body)
        assert_in('<li><a href="//www.data.gov/contact">Contact</a></li>', index_response.unicode_body)

    def test_datagovtheme_topics(self):
        app = self._get_test_app()

        index_response = app.get('/dataset')

        assert_in('<li class="menu-agriculture">', index_response.unicode_body)
        assert_in('<li class="menu-climate">', index_response.unicode_body)
        assert_in('<li class="menu-ecosystems">', index_response.unicode_body)
        assert_in('<li class="menu-energy">', index_response.unicode_body)
        assert_in('<li class="menu-local-government">', index_response.unicode_body)
        assert_in('<li class="menu-maritime">', index_response.unicode_body)
        assert_in('<li class="menu-ocean">', index_response.unicode_body)
        
    def test_datagovtheme_organizations(self):
        app = self._get_test_app()

        index_response = app.get('/organization')

        assert_in("No organizations found", index_response.unicode_body)
        assert_in("Search organizations...", index_response.unicode_body)
        assert_in("What are organizations?", index_response.unicode_body)


