# encoding: utf-8
import logging
import re

import mock
import pytest

from ckanext.datagovtheme import helpers


################
# get_login_url
################


@pytest.mark.ckan_config('ckanext.saml2auth.enable_ckan_internal_login', 'false')
def test_saml2_login_url():
    """ test saml2 URL on Catalog-next """
    actual_login_url = helpers.get_login_url()
    assert '/user/saml2login' == actual_login_url


@pytest.mark.ckan_config('ckanext.saml2auth.enable_ckan_internal_login', 'true')
def test_login_url():
    """ test saml2 URL on Catalog-next """
    actual_login_url = helpers.get_login_url()
    assert '/user/login' == actual_login_url

##############
# api_doc_url
##############


@mock.patch('ckanext.datagovtheme.helpers.h')
def test_api_doc_url(mock_ckan_lib_helpers):
    mock_ckan_lib_helpers.lang.return_value = 'en'
    mock_ckan_lib_helpers.ckan_version.return_value = '2.8.7'

    api_doc_url = helpers.api_doc_url()

    assert 'https://docs.ckan.org/en/2.8/api/index.html' == api_doc_url

##################
# get_bureau_info
##################


def assert_url(actual_url, expected_bureau_code):
    # In CKAN 2.9, the url_for is returning a path ending in / which does not
    # happen in 2.8. Include an optional ending / in the path, use URL encoded
    # characters.
    bureau_url_re = re.compile('/dataset/?\\?q=bureauCode%3A%22(?P<agency_part>[0-9]{3})%3A(?P<bureau_part>[0-9]{2})%22')

    match = bureau_url_re.match(actual_url)
    assert match, 'URL should match pattern /dataset?q=bureauCode:"000:00"'

    agency_part = match.group('agency_part')
    bureau_part = match.group('bureau_part')
    assert "%s:%s" % (agency_part, bureau_part) == expected_bureau_code


def test_get_bureau_info_blm():
    bureau_code = '010:04'
    bureau_info = helpers.get_bureau_info(bureau_code)

    assert bureau_info['title'] == 'Bureau of Land Management'
    assert bureau_info['code'] == bureau_code
    assert bureau_info['logo'] == '/images/logos/010-04.png'
    assert_url(bureau_info['url'], bureau_code)


def test_get_bureau_info_logo_jpg():
    """Assert that bureau logos as jpg are found."""
    bureau_code = '418:00'
    bureau_info = helpers.get_bureau_info(bureau_code)

    assert bureau_info['title'] == 'National Endowment for the Humanities'
    assert bureau_info['code'] == bureau_code
    assert bureau_info['logo'] == '/images/logos/418-00.jpg'
    assert_url(bureau_info['url'], bureau_code)


def test_get_bureau_info_logo_missing():
    """Assert that bureaus with missing logos are still identified."""
    bureau_code = '915:00'
    bureau_info = helpers.get_bureau_info(bureau_code)

    assert bureau_info['title'] == 'Federal National Mortgage Association'
    assert bureau_info['code'] == bureau_code
    assert bureau_info['logo'] is None
    assert_url(bureau_info['url'], bureau_code)


def test_get_bureau_info_list():
    """Given a list of bureau codes, the first code is assumed."""
    bureau_code = '010:04'
    bureau_info = helpers.get_bureau_info([bureau_code, '418:00'])

    assert bureau_info['title'] == 'Bureau of Land Management'
    assert bureau_info['code'] == bureau_code
    assert bureau_info['logo'] == '/images/logos/010-04.png'
    assert_url(bureau_info['url'], bureau_code)


def test_get_bureau_info_invalid():
    """Assert None is returned and a warning is logged."""
    helpers_logger = logging.getLogger('ckanext.datagovtheme.helpers')
    with mock.patch.object(helpers_logger, 'warning') as mock_log_warning:
        bureau_info = helpers.get_bureau_info('01004')

        assert bureau_info is None
        mock_log_warning.assert_called_once_with('bureau code is invalid code=01004')


def test_get_bureau_info_none():
    """Assert None is returned"""
    bureau_info = helpers.get_bureau_info(None)

    assert bureau_info is None
