#!/bin/bash
set -e

echo "Updating script ..."

wget https://raw.githubusercontent.com/GSA/catalog.data.gov/master/tools/ci-scripts/circleci-build-catalog-next.bash
wget https://raw.githubusercontent.com/GSA/catalog.data.gov/master/ckan/test-catalog-next.ini

sudo chmod +x circleci-build-catalog-next.bash
source circleci-build-catalog-next.bash

echo "Update ckanext-datagovtheme"
python setup.py develop

echo "Install dev.requirements"
pip install -r dev-requirements.txt

echo "TESTING ckanext-datagovtheme"
nosetests --ckan --with-pylons=test-catalog-next.ini ckanext/datagovtheme --debug=ckanext
