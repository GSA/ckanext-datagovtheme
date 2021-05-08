# encoding: utf-8
from builtins import object
import pytest

from ckantoolkit.tests import factories


@pytest.mark.usefixtures('clean_db', 'clean_index')
class TestNotes(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_datagovtheme_html_loads(self, app):

        notes = 'Notes for a test dataset'
        dataset = factories.Dataset(notes=notes)

        dataset_response = app.get('/dataset/{}'.format(dataset['name']))

        assert '<div itemprop="description" class="notes embedded-content">' in dataset_response.unicode_body
        assert notes in dataset_response.unicode_body
