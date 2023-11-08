import time

import pytest
from bs4 import BeautifulSoup
from ckantoolkit.tests import factories


# The /dataset page uses get_pkg_dict_extra which depends on HarvestObject,
# hence the harvest extension. Include it for these tests.
@pytest.mark.ckan_config("ckan.plugins", "harvest datagovtheme spatial_metadata")
@pytest.mark.use_fixtures("with_plugins", "clean_db", "clean_index")
class TestSearchFilters:
    @pytest.fixture(autouse=True)
    def setup(self):
        uid = str(int(time.time()) + 2)
        name = "test_org" + uid
        self.organization = factories.Organization(
            name=name,
            extras=[
                {"key": "email_list", "value": "test@datagovhelp.gov"},
                {"key": "something_important", "value": "blah"},
            ],
        )
        group_1 = "test_group_1" + uid
        group_2 = "test_group_2" + uid
        self.group1 = factories.Group(name=group_1)
        self.group2 = factories.Group(name=group_2)
        dataset_1 = "test_dataset_1" + uid
        dataset_2 = "test_dataset_2" + uid
        self.dataset1 = factories.Dataset(
            name=dataset_1,
            owner_org=self.organization["id"],
            groups=[{"name": self.group1["name"]}],
        )
        self.dataset2 = factories.Dataset(
            name=dataset_2,
            owner_org=self.organization["id"],
            groups=[{"name": self.group2["name"]}],
        )

    def test_not_empty_sections(self, app):
        index_response = app.get("/dataset")

        html = BeautifulSoup(index_response.body, "html.parser")

        # get the main section where filters are included
        filters = html.select_one("div.filters")
        assert filters, "Could not find div.filters"

        # Get the section "names"
        filter_names = [
            " ".join(filter_header.stripped_strings)
            for filter_header in filters.select("section.module .module-heading")
        ]
        assert len(filter_names) > 0, "Could not find section.module .module-heading"

        assert "Organizations" in filter_names
        assert "Tags" in filter_names
        assert "Bureaus" in filter_names
        assert "Publishers" in filter_names

    def test_email_list_not_public(self, app):
        index_response = app.get("/organization/about/" + self.organization["name"])

        html = BeautifulSoup(index_response.body, "html.parser")

        extras_table = html.select("th.dataset-label")
        extras_keys = [i.text for i in extras_table]
        assert extras_keys == ["something_important"]
        assert "email_list" not in extras_keys


class TestApiLinks(object):
    def test_api_doc_link(self, app):
        """Assert CKAN major/minor version matches API docs URL."""
        # TODO mock helpers.api_doc_url and then assert the mock was called
        # after the request. Is this possible in CKAN?
        from ckan.lib.helpers import ckan_version

        expected_version = ".".join(ckan_version().split(".")[0:2])

        index_response = app.get("/dataset")
        html = BeautifulSoup(index_response.body, "html.parser")

        # Test link to api docs matches CKAN version
        api_doc_href = html.find("a", string="API Docs")["href"]
        assert expected_version in api_doc_href

    def test_api_url(self, app):
        """Assert API link on dataset page."""
        index_response = app.get("/dataset")

        html = BeautifulSoup(index_response.body, "html.parser")
        api_href = html.find("a", string="API")["href"]
        assert "/api/3" == api_href


# This test probably can't run because the javascript doesn't load
# in the same way as the browser runs it.  The map relies on the
# javascript running.
# class TestMapLoading(object):
#     def test_map_html(self, app):
#         index_response = app.get('/dataset')
#         html = BeautifulSoup(index_response.body, 'html.parser')
#
#         map_div_elements = html.find(id='dataset-map'). \
#             find('div', {'class': 'dataset-map'}). \
#             find(id='dataset-map-container'). \
#             contents
#
#         assert len(map_div_elements) > 0
