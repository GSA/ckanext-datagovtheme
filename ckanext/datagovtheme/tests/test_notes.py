# encoding: utf-8
import time
import pytest

from ckantoolkit.tests import factories


# The /dataset page uses get_pkg_dict_extra which depends on HarvestObject,
# hence the harvest extension. Include it for these tests.
@pytest.mark.ckan_config('ckan.plugins', 'harvest datagovtheme')
@pytest.mark.use_fixtures('with_plugins', 'clean_db', 'clean_index')
class TestNotes(object):
    '''Tests for the ckanext.datagovtheme.plugin module.'''

    def test_datagovtheme_html_loads(self, app):

        notes = 'Notes for a test dataset'
        name = 'random_test' + str(int(time.time()))
        dataset = factories.Dataset(notes=notes, name=name)

        dataset_response = app.get('/dataset/{}'.format(dataset['name']))

        assert '<div itemprop="description" class="notes embedded-content">' in dataset_response.body
        assert notes in dataset_response.body
