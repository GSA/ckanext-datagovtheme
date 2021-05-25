# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
from builtins import object


class TestDatagovthemeServed(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_datagovtheme_css_file(self, app):
        """Assert the correct version of CSS is served."""
        index_response = app.get('/dataset')

        # Note: in development/debug mode, this asset uses the output filename
        # in webassets.yml. In production mode, it is compiled to a different
        # name and may have addtional filters (e.g. minification) applied.
        assert 'datagovtheme.css' in index_response.body

    def test_datagovtheme_html_loads(self, app):
        index_response = app.get('/dataset')

        assert "Search Data.Gov" in index_response.body
        assert "Search datasets..." in index_response.body
        assert "No datasets found" in index_response.body

    def test_datagovtheme_navigation(self, app):
        index_response = app.get('/dataset')

        assert '<li class="active"><a href="/dataset">Data</a></li>' in index_response.body
        assert '<a class="dropdown-toggle" data-toggle="dropdown">Topics<b\n            class="caret"></b></a>' \
               in index_response.body
        assert '<li><a href="//resources.data.gov">Resources</a></li>' in index_response.body
        assert '<li><a href="//strategy.data.gov">Strategy</a></li>' in index_response.body
        assert '<li><a href="//www.data.gov/developers/">Developers</a></li>' in index_response.body
        assert '<li><a href="//www.data.gov/contact">Contact</a></li>' in index_response.body

    def test_datagovtheme_topics(self, app):
        index_response = app.get('/dataset')

        assert '<li class="menu-agriculture">' in index_response.body
        assert '<li class="menu-climate">' in index_response.body
        assert '<li class="menu-energy">' in index_response.body
        assert '<li class="menu-local-government">' in index_response.body
        assert '<li class="menu-maritime">' in index_response.body
        assert '<li class="menu-ocean">' in index_response.body
        assert '<li class="menu-older-adults-health">' in index_response.body

    def test_datagovtheme_organizations(self, app):
        index_response = app.get('/organization')

        assert "No organizations found" in index_response.body
        assert "Search organizations..." in index_response.body
        assert "What are organizations?" in index_response.body
