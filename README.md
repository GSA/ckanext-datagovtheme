# ckanext-datagovtheme
This repository is front end code sepration for catalog.data.gov. This contains all the template files, Javascripts and stylesheets.

The [ckanext-geodatagov](https://github.com/GSA/ckanext-geodatagov) and [ckanext-spatial](https://github.com/ckan/ckanext-spatial) extensions must be [installed and enabled](https://docs.ckan.org/en/2.8/extensions/tutorial.html#installing-the-extension) as plugins before this extension can be installed and enabled.

This extension as well as the dependent extensions above must be installed properly with CKAN before running the tests for this extension.

The tests for this extension are located in the [test directory](/ckanext/datagovtheme/tests/test_datagovetheme.py).

They follow the guidelines for [testing CKAN extensions](https://docs.ckan.org/en/2.8/extensions/testing-extensions.html#testing-extensions).

To run the extension tests, cd into the ckanext-datagovtheme directory and run this command:

`nosetests --ckan --with-pylons=test.ini ckanext/datagovthem/tests`