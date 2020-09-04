#!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "-----------------------------------------------------------------"
echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
sudo apt-get install solr-jetty libcommons-fileupload-java libpq-dev postgresql postgresql-contrib swig libgeos-dev

echo "-----------------------------------------------------------------"
echo "Installing CKAN and its dependencies..."

cd .. # CircleCI starts inside ckanext-datajson folder
pwd
ls -la

git clone https://github.com/GSA/ckan
cd ckan
git checkout datagov

echo "-----------------------------------------------------------------"
echo "Installing Python dependencies..."

pip install --upgrade pip
pip install setuptools -U

python setup.py develop
# TODO remove after upgrading to CKAN 2.8
cp ./ckan/public/base/css/main.css ./ckan/public/base/css/main.debug.css
pip install wheel

# install all from catalog-app repo
pip install -r https://raw.githubusercontent.com/GSA/catalog-app/master/requirements-freeze.txt

cd ..
echo "-----------------------------------------------------------------"
echo "Setting up Solr..."
# solr is multicore for tests on ckan master now, but it's easier to run tests
# on Travis single-core still.
# see https://github.com/ckan/ckan/issues/2972
sed -i -e 's/solr_url.*/solr_url = http:\/\/127.0.0.1:8983\/solr/' ckan/test-core.ini
printf "NO_START=0\nJETTY_HOST=127.0.0.1\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | sudo tee /etc/default/jetty
sudo cp ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service jetty restart

echo "-----------------------------------------------------------------"
echo "Creating the PostgreSQL user and database..."
sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
sudo -u postgres psql -c 'CREATE DATABASE ckan_test WITH OWNER ckan_default;'
sudo -u postgres psql -c 'CREATE DATABASE datastore_test WITH OWNER ckan_default;'

echo "-----------------------------------------------------------------"
echo "Initialising the database..."
cd ckan
paster db init -c test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the report ..."
paster --plugin=ckanext-report report initdb -c ../ckan/test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the archiver ..."
paster --plugin=ckanext-archiver archiver init -c ../ckan/test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the harvester ..."
paster --plugin=ckanext-harvest harvester initdb -c ../ckan/test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the qa ..."
paster --plugin=ckanext-qa qa init -c ../ckan/test-core.ini

cd ..
echo "-----------------------------------------------------------------"
echo "Installing ckanext-datagovtheme and its requirements..."
cd ckanext-datagovtheme
python setup.py develop

echo "travis-build.bash is done."