# encoding: utf-8
from nose.tools import assert_in
from mock import patch
import pytest

try:
    from ckan.plugins.toolkit import config
except ImportError:
    from pylons import config

from ckan import plugins as p


class TestLoginURL(object):

    def test_base_login(self, app):
        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'true'
        index_response = app.get('/dataset')
        assert_in('/user/login', index_response.unicode_body)

    @pytest.mark.ckan_config('ckanext.saml2auth.enable_ckan_internal_login', 'true')
    @patch('ckan.plugins')
    def test_saml2_login_url(self, app, mock_plugins):
        """ test saml2 URL on Catalog-next """
        if p.toolkit.check_ckan_version(min_version='2.8'):
            mock_plugins.plugin_loaded.return_value = True
            index_response = app.get('/dataset')

            assert_in('/user/saml2login', index_response.unicode_body)

    @pytest.mark.ckan_config('ckanext.saml2auth.enable_ckan_internal_login', 'false')
    def test_login_url(self, app):
        """ test saml2 URL on Catalog-next """
        if p.toolkit.check_ckan_version(min_version='2.8'):
            index_response = app.get('/dataset')

            assert_in('/user/login', index_response.unicode_body)
