# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
import ckan.plugins
import paste.fixture
import pylons.test


class TestDatagovthemeServed(object):
    '''Tests for the ckanext.example_iauthfunctions.plugin module.

    '''
    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''

        # Make the Paste TestApp that we'll use to simulate HTTP requests to
        # CKAN.
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)

        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        ckan.plugins.load('geodatagov')
        ckan.plugins.load('datagovtheme')

    @classmethod
    def teardown_class(cls):
        ckan.plugins.unload('geodatagov')
        ckan.plugins.unload('datagovtheme')

    def test_plugin_loaded(self):
        assert ckan.plugins.plugin_loaded('datagovtheme')
        assert ckan.plugins.plugin_loaded('geodatagov')

    def test_datagovtheme_css(self):
        app = self.app

        index_response = app.get('/dataset')

        assert 'datagovtheme_bootstrap2.css' in index_response, index_response
        assert 'datagovtheme.css' not in index_response
