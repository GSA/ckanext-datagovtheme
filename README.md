# ckanext-datagovtheme

[![CircleCI](https://circleci.com/gh/GSA/ckanext-datagovtheme.svg?style=svg)](https://circleci.com/gh/GSA/ckanext-datagovtheme)

This repository is front end code sepration for catalog.data.gov. This contains all the template files, Javascripts and stylesheets.

The [ckanext-geodatagov](https://github.com/GSA/ckanext-geodatagov) and [ckanext-spatial](https://github.com/ckan/ckanext-spatial) extensions must be [installed and enabled](https://docs.ckan.org/en/2.8/extensions/tutorial.html#installing-the-extension) as plugins before this extension can be installed and enabled.

This extension is compatible with versions of CKAN using Bootstrap 2 and Bootstrap 3. If CKAN is using version 2.8 or higher this extension will use Bootstrap 3.

This extension as well as the dependent extensions above must be installed properly with CKAN before running the tests for this extension.

The tests for this extension are located in the [test directory](/ckanext/datagovtheme/tests/test_datagovetheme.py).

They follow the guidelines for [testing CKAN extensions](https://docs.ckan.org/en/2.8/extensions/testing-extensions.html#testing-extensions).

To run the extension tests:

1. Make sure your virtual environment is activated

`. /usr/lib/ckan/default/bin/activate`

2. cd into the ckanext-datagovtheme directory

`cd /usr/lib/ckan/default/src/ckanext-datagovtheme`

3. Use the nosetests command:

`nosetests --ckan --with-pylons=test.ini ckanext/datagovtheme/tests`

Note: the tests will only run if the environment is installed using the [CKAN Install from Source](https://docs.ckan.org/en/2.8/maintaining/installing/install-from-source.html#installing-ckan-from-source) installation
