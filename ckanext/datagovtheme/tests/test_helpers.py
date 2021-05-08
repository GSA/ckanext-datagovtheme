# encoding: utf-8
import mock

try:
    from ckan.tests.helpers import FunctionalTestBase
    from ckan.plugins.toolkit import config
except ImportError:
    from ckan.new_tests.helpers import FunctionalTestBase
    from pylons import config

from ckanext.datagovtheme import helpers


class TestGetLoginUrl(FunctionalTestBase):

    def test_saml2_login_url(self):
        """ test saml2 URL on Catalog-next """
        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'false'

        actual_login_url = helpers.get_login_url()
        assert '/user/saml2login' == actual_login_url

    def test_login_url(self):
        """ test saml2 URL on Catalog-next """
        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'true'

        actual_login_url = helpers.get_login_url()
        assert '/user/login' == actual_login_url


class TestApiDocUrl(FunctionalTestBase):

    @mock.patch('ckanext.datagovtheme.helpers.h')
    def test_api_doc_url(self, mock_ckan_lib_helpers):
        mock_ckan_lib_helpers.lang.return_value = 'en'
        mock_ckan_lib_helpers.ckan_version.return_value = '2.8.7'

        api_doc_url = helpers.api_doc_url()

        assert 'https://docs.ckan.org/en/2.8/api/index.html' == api_doc_url
