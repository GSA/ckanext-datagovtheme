# encoding: utf-8
from nose.tools import assert_in

try:
    from ckan.tests.helpers import FunctionalTestBase
    from ckan.plugins.toolkit import config
except ImportError:
    from ckan.new_tests.helpers import FunctionalTestBase
    from pylons import config

from ckan import plugins as p


class TestLoginURL(FunctionalTestBase):

    def test_base_login(self):
        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'true'
        app = self._get_test_app()
        index_response = app.get('/dataset')
        assert_in('/user/login', index_response.unicode_body)

    def test_saml2_login_url(self):
        """ test saml2 URL on Catalog-next """
        if not p.plugin_loaded('saml2auth'):
            p.load('saml2auth')

        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'false'

        app = self._get_test_app()
        index_response = app.get('/dataset')

        assert_in('/user/saml2login', index_response.unicode_body)

    def test_login_url(self):
        """ test saml2 URL on Catalog-next """
        config['ckanext.saml2auth.enable_ckan_internal_login'] = 'false'
        if p.plugin_loaded('saml2auth'):
            p.unload('saml2auth')

        app = self._get_test_app()
        index_response = app.get('/dataset')

        assert_in('/user/login', index_response.unicode_body)
