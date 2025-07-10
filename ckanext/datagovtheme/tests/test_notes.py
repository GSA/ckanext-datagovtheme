# encoding: utf-8
import time

import pytest
from ckantoolkit.tests import factories


@pytest.mark.ckan_config(
    "ckan.plugins", "geodatagov datagovtheme spatial_metadata"
)
@pytest.mark.use_fixtures("with_plugins", "clean_db", "clean_index")
class TestNotes(object):
    """Tests for the ckanext.datagovtheme.plugin module."""

    def test_datagovtheme_html_loads(self, app):

        notes = "Notes for a test dataset"
        name = "random_test" + str(int(time.time()))
        organization = factories.Organization(name="myorg2")
        dataset = factories.Dataset(
            notes=notes, name=name, owner_org=organization["id"]
        )

        dataset_response = app.get("/dataset/{}".format(dataset["name"]))

        assert (
            '<div itemprop="description" class="notes embedded-content">'
            in dataset_response.body
        )
        assert notes in dataset_response.body

    def test_datagovtheme_escapes_notes(self, app):
        notes = 'Notes with a quote (")'
        name = 'random_test' + str(int(time.time()))
        organization = factories.Organization(name=name)
        dataset = factories.Dataset(notes=notes, name=name, owner_org=organization['id'])

        dataset_response = app.get('/dataset/{}'.format(dataset['name']))

        # JSON-LD element needs to escape the quote mark in notes
        print(dataset_response.body)
        assert '"description": "Notes with a quote (\\")"' in dataset_response.body
