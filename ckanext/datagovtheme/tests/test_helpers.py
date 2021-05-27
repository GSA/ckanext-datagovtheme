# encoding: utf-8
from builtins import object
import mock
import pytest


from ckanext.datagovtheme import helpers


class TestGetLoginUrl(object):

    @pytest.mark.ckan_config('ckanext.saml2auth.enable_ckan_internal_login', 'false')
    def test_saml2_login_url(self):
        """ test saml2 URL on Catalog-next """
        actual_login_url = helpers.get_login_url()
        assert '/user/saml2login' == actual_login_url

    @pytest.mark.ckan_config('ckanext.saml2auth.enable_ckan_internal_login', 'true')
    def test_login_url(self):
        """ test saml2 URL on Catalog-next """
        actual_login_url = helpers.get_login_url()
        assert '/user/login' == actual_login_url


class TestApiDocUrl(object):

    @mock.patch('ckanext.datagovtheme.helpers.h')
    def test_api_doc_url(self, mock_ckan_lib_helpers):
        mock_ckan_lib_helpers.lang.return_value = 'en'
        mock_ckan_lib_helpers.ckan_version.return_value = '2.8.7'

        api_doc_url = helpers.api_doc_url()

        assert 'https://docs.ckan.org/en/2.8/api/index.html' == api_doc_url


class TestBureauCodeTransform(object):

    @mock.patch('ckanext.datagovtheme.helpers.h')
    def test_get_bureau_info(self, mock_ckan_lib_helpers):

        bureau_info = helpers.get_bureau_info("010:04")

        assert bureau_info.title == "Bureau of Land Management"
