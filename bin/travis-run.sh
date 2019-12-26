#!/bin/sh -e

echo "TESTING ckanext-datagovtheme"

echo "pip list"
pip list

echo "pip freeze"
pip freeze

nosetests --ckan --with-pylons=test.ini ckanext/datagovtheme/tests

