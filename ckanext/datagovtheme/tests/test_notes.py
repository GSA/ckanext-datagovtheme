# encoding: utf-8
from nose.tools import assert_in, assert_true, assert_not_in, assert_false

try:
    from ckan.tests.helpers import FunctionalTestBase, reset_db
    from ckan.tests import factories
except ImportError:
    from ckan.new_tests.helpers import FunctionalTestBase, reset_db
    from ckan.new_tests import factories


class TestNotes(FunctionalTestBase):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_datagovtheme_html_loads(self):

        notes = 'Notes for a test dataset'
        dataset = factories.Dataset(notes=notes)
        app = self._get_test_app()

        dataset_response = app.get('/dataset/{}'.format(dataset['name']))
    
        assert_in('<div itemprop="description" class="notes embedded-content">', dataset_response.unicode_body)
        assert_in('notes', dataset_response.unicode_body)
