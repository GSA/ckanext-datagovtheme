# encoding: utf-8

'''Tests for the ckanext.datagovtheme extension.

'''
import pytest

import ckanext


@pytest.mark.ckan_config('ckan.plugins', 'datagovtheme')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestDatagovthemeServed(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_datagovtheme_simple(self, app):
        index_response = app.get('/dataset')

        assert 'DOCTYPE' in index_response.body


    def test_datagovtheme_css_file(self, app):
        index_response = app.get('/dataset')

        if ckanext.datagovtheme.helpers.is_bootstrap2():
            assert 'datagovtheme_bootstrap2.css' in index_response.body
            assert 'datagovtheme.css' in index_response.body
        else:
            assert 'datagovtheme.css' in index_response.body
            assert 'datagovtheme_bootstrap2.css' in index_response.body

    def test_datagovtheme_html_loads(self, app):
        index_response = app.get('/dataset')

        assert "Search Data.Gov" in index_response.body
        assert "Search datasets..." in index_response.body
        assert "No datasets found" in index_response.body

    def test_datagovtheme_navigation(self, app):
        index_response = app.get('/dataset')

        assert '<li class="active"><a href="/dataset">Data</a></li>' in index_response.body
        assert '<a class="dropdown-toggle" data-toggle="dropdown">Topics<b\n            class="caret"></b></a>' in \
               index_response.body
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
