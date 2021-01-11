# encoding: utf-8
from nose.tools import assert_in

try:
    from ckan.tests.helpers import FunctionalTestBase
    from ckan.tests import factories
except ImportError:
    from ckan.new_tests.helpers import FunctionalTestBase
    from ckan.new_tests import factories


class TestNotes(FunctionalTestBase):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_datagovtheme_html_loads(self):

        notes = 'Notes for a test dataset'
        dataset = factories.Dataset(notes=notes)
        app = self._get_test_app()

        dataset_response = app.get('/dataset/{}'.format(dataset['name']))

        assert_in('<div itemprop="description" class="notes embedded-content">', dataset_response.unicode_body)
        assert_in(notes, dataset_response.unicode_body)
