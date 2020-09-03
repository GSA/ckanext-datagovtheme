#!/bin/sh -e

echo "TESTING ckanext-datagovtheme with CKAN 2.3 and Bootstrap 2"

nosetests --ckan --with-pylons=test-catalog-2.3.ini ckanext/datagovtheme/tests --nologcapture

