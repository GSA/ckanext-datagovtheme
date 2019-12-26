#!/bin/sh -e

echo "TESTING ckanext-datagovtheme 2.3"

nosetests --ckan --with-pylons=test.ini ckanext/datagovtheme/tests/test_datagovtheme_23.py

