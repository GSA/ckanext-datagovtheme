# encoding: utf-8
try:
    from ckan.tests.helpers import FunctionalTestBase
    from ckan.plugins.toolkit import config
except ImportError:
    from ckan.new_tests.helpers import FunctionalTestBase
    from pylons import config

from ckan import plugins as p
from ckanext.datagovtheme import helpers


class TestGetLoginUrl(FunctionalTestBase):

    def test_base_login(self):
        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'true'
        actual_login_url = helpers.get_login_url()
        assert '/user/login' == actual_login_url

    def test_saml2_login_url(self):
        """ test saml2 URL on Catalog-next """
        if not p.plugin_loaded('saml2auth'):
            p.load('saml2auth')

        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'false'

        actual_login_url = helpers.get_login_url()
        assert '/user/saml2login' == actual_login_url

    def test_login_url(self):
        """ test saml2 URL on Catalog-next """
        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'false'
        if p.plugin_loaded('saml2auth'):
            p.unload('saml2auth')

        actual_login_url = helpers.get_login_url()
        assert '/user/login' == actual_login_url
