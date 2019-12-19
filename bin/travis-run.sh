#!/bin/sh -e

echo "TESTING ckanext-datagovtheme"

nosetests --ckan --with-pylons=subdir/test.ini ckanext/datagovtheme 