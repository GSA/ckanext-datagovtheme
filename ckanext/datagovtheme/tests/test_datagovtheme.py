# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
from ckantoolkit.tests.helpers import FunctionalTestBase
from nose.tools import assert_in, assert_true, assert_not_in, assert_false

from ckan import plugins as p
import mock
import ckanext.datagovtheme.helpers.is_bootstrap2


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

    @mock.patch(ckanext.datagovtheme.helpers.is_bootstrap2, mock.MagicMock(return_value=False))
    def test_datagovtheme_css_is_bootstrap2(self):
        app = self._get_test_app()

        index_response = app.get('/dataset')
        is_bootstrap2 = ckanext.datagovtheme.helpers.is_bootstrap2
        if is_bootstrap2():
            assert_in('datagovtheme_bootstrap2.css', index_response.unicode_body)
            assert_not_in('datagovtheme.css', index_response.unicode_body) 
    
    @mock.patch(ckanext.datagovtheme.helpers.is_bootstrap2, mock.MagicMock(return_value=False))
    def test_datagovtheme_css(self):
        app = self._get_test_app()

        index_response = app.get('/dataset')
        is_bootstrap2 = ckanext.datagovtheme.helpers.is_bootstrap2
        if not is_bootstrap2():
            assert_in('datagovtheme.css', index_response.unicode_body)
            assert_not_in('datagovtheme_bootstrap2.css', index_response.unicode_body)


