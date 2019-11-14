# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
from bs4 import BeautifulSoup
from nose.tools import assert_true

import ckan.tests.helpers as helpers


class TestDatagovthemeServed(helpers.FunctionalTestBase):
    '''Tests for the ckanext.datagovtheme.plugin module.'''
    
    def plugin_loaded(self):
        assert_true(ckan.plugins.plugin_loaded('datagovtheme'))

    def test_datagovtheme_css(self):
        app = helpers._get_test_app()

        index_response = app.get('/')

        assert_true('datagovtheme.js' in index_response)
        assert_true('datagovtheme.css' in index_response)
