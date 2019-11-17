# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
from bs4 import BeautifulSoup
from nose.tools import assert_true

import ckan.tests.helpers as helpers


class TestDatagovthemeServed(helpers.FunctionalTestBase):
    '''Tests for the ckanext.datagovtheme.plugin module.'''
    
    def test_plugin_loaded(self):
        ckan.plugins.load('geodatagov')
        assert_true(ckan.plugins.plugin_loaded('geodatagov'))

        ckan.plugins.load('datagovtheme')
        assert_true(ckan.plugins.plugin_loaded('datagovtheme'))

    def test_datagovtheme_css(self):
        ckan.plugins.load('geodatagov')
        ckan.plugins.load('datagovtheme')
        app = helpers._get_test_app()

        index_response = app.get('/')

        assert_true('main.min.css' in index_response)
