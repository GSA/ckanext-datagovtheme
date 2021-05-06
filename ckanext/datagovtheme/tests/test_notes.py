# encoding: utf-8
from nose.tools import assert_in

from ckantoolkit.tests import factories


class TestNotes(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_datagovtheme_html_loads(self, app):

        notes = 'Notes for a test dataset'
        dataset = factories.Dataset(notes=notes)

        dataset_response = app.get('/dataset/{}'.format(dataset['name']))

        assert_in('<div itemprop="description" class="notes embedded-content">', dataset_response.unicode_body)
        assert_in(notes, dataset_response.unicode_body)
