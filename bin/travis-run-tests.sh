#!/bin/sh -e

echo "TESTING ckanext-datagovtheme with CKAN 2.8 and Bootstrap 3"

nosetests --ckan --with-pylons=test.ini ckanext/datagovtheme/tests/test_datagovtheme.py --nologcapture

