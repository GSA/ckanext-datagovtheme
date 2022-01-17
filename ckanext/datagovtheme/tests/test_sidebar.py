# encoding: utf-8
from builtins import object
import pytest
import time

from ckantoolkit.tests import factories


# The /dataset page uses get_pkg_dict_extra which depends on HarvestObject,
# hence the harvest extension. Include it for these tests.
@pytest.mark.ckan_config('ckan.plugins', 'harvest datagovtheme')
@pytest.mark.use_fixtures('with_plugins', 'clean_db', 'clean_index')
class TestNotes(object):
    '''Tests for the sidebars of catalog.'''

    def create_datasets(self):
        uid = str(int(time.time()) + 1)
        self.sysadmin = factories.Sysadmin(name='admin')
        name = "test_org" + uid
        self.organization = factories.Organization(name=name)
        group_1 = "test_group_1" + uid
        self.group1 = factories.Group(name=group_1)
        self.dataset_1 = "test_dataset_1" + uid
        self.dataset1 = {
            'name': 'my_package_000',
            'title': 'my package',
            'notes': 'my package notes',
            'public_access_level': 'public',
            'access_level_comment': 'Access level comment',
            'unique_id': '000',
            'contact_name': 'Jhon',
            'program_code': '018:001',
            'bureau_code': '019:20',
            'contact_email': 'jhon@mail.com',
            'publisher': 'Publicher 01',
            'modified': '2019-01-27 11:41:21',
            'tag_string': 'mypackage,tag01,tag02',
            'parent_dataset': 'true',
            'owner_org': self.organization['id'],
            'groups': [{"name": self.group1["name"]}]
        }

        for key in self.sysadmin:
            if key not in ['id', 'name']:
                self.dataset1.update({key: self.sysadmin[key]})
        self.dataset1 = factories.Dataset(**self.dataset1)

    def test_sidebar_click(self):
        self.create_datasets()
