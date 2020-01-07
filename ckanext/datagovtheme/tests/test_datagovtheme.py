# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
from ckantoolkit.tests.helpers import FunctionalTestBase
from nose.tools import assert_in, assert_true, assert_not_in

from ckan import plugins as p


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

        assert_in('datagovtheme.css', index_response.unicode_body)
        assert_not_in('datagovtheme_bootstrap2.css', index_response.unicode_body)
