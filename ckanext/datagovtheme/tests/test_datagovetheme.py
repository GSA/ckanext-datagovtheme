# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
from nose.tools import assert_true, assert_in

from ckan import plugins as p
from ckan.plugins import toolkit
from ckantoolkit.tests.helpers import _get_test_app, FunctionalTestBase

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

    def test_datagovtheme_css(self):
        app = self._get_test_app()

        index_response = app.get('/dataset')

        if p.toolkit.check_ckan_version(min_version='2.8'):
            assert_in('datagovtheme28.css', index_response.unicode_body)
        else:
            assert_in('datagovtheme.css', index_response.unicode_body)
