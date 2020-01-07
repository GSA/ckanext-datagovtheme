#!/bin/sh -e

echo "TESTING ckanext-datagovtheme with CKAN 2.3 and Bootstrap 2"

nosetests --ckan --with-pylons=test.ini ckanext/datagovtheme/tests/test_datagovtheme_bootstrap2.py --nologcapture

