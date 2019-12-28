#!/bin/sh -e

echo "TESTING ckanext-datagovtheme 2.8"

nosetests --ckan --with-pylons=test.ini ckanext/datagovtheme/tests/test_datagovtheme_28.py

