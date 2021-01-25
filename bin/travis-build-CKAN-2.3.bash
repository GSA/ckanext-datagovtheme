#!/bin/bash
set -e

echo "This is travis-build.bash..."
echo "-----------------------------------------------------------------"

echo "Moving to Python 2.7.10"
sudo apt-get update -qq
sudo apt-get install -y gcc-multilib g++-multilib libffi-dev libffi6 libffi6-dbg \
    python-crypto python-mox3 python-pil python-ply libssl-dev zlib1g-dev libbz2-dev \
    libexpat1-dev libbluetooth-dev libgdbm-dev dpkg-dev quilt autotools-dev \
    libreadline-dev libtinfo-dev libncursesw5-dev tk-dev blt-dev libssl-dev zlib1g-dev \
    libbz2-dev libexpat1-dev libbluetooth-dev libsqlite3-dev libgpm2 mime-support \
    netbase net-tools bzip2 solr-jetty libcommons-fileupload-java libpq-dev \
    postgresql postgresql-contrib swig libgeos-dev python-pastescript

wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar xvf Python-2.7.10.tgz
cd Python-2.7.10/

./configure --prefix /usr/local/lib/python2.7.10 --enable-ipv6 --enable-unicode=ucs4
make
sudo make install

sudo rm /usr/bin/python
sudo ln -s /usr/local/lib/python2.7.10/bin/python /usr/bin/python
export PATH="/usr/local/lib/python2.7.10/bin:$PATH"

cd ..
# -------------------
echo 'Getting Python version:'
python -V

echo 'Getting Python path:'
which python

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
sudo python get-pip.py

echo 'Preparing PIP ...'
sudo -H python -m pip install pip==20.3.3
sudo -H python -m pip install setuptools==44.1.1
sudo -H python -m pip install wheel

echo "nosetests"
sudo -H python -m pip install nose
which nosetests

echo "-----------------------------------------------------------------"
echo "Installing CKAN and its dependencies..."
# install all from catalog-app repo
wget https://raw.githubusercontent.com/GSA/catalog-app/master/requirements-freeze.txt
sed -i '/saml2/d' requirements-freeze.txt
sudo -H python -m pip install -r requirements-freeze.txt
sudo -H python -m pip install -U repoze.who==2.0 Paste==1.7.5.1

echo "Cloning CKAN ..."
cd .. # CircleCI starts inside ckanext-datagovtheme folder
pwd
ls -la

git clone https://github.com/GSA/ckan
cd ckan
git checkout datagov

echo "-----------------------------------------------------------------"
echo "Installing CKAN ..."

# TODO remove after upgrading to CKAN 2.8
cp ./ckan/public/base/css/main.css ./ckan/public/base/css/main.debug.css

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

echo "-----------------------------------------------------------------"
echo "Initialising the database..."
cd ckan
sudo paster --plugin=ckan db init -c test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the report ..."
sudo paster --plugin=ckanext-report report initdb -c test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the archiver ..."
sudo paster --plugin=ckanext-archiver archiver init -c test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the harvester ..."
sudo paster --plugin=ckanext-harvest harvester initdb -c test-core.ini
echo "-----------------------------------------------------------------"
echo "Initialising the qa ..."
sudo paster --plugin=ckanext-qa qa init -c test-core.ini

cd ..
echo "-----------------------------------------------------------------"
echo "Installing ckanext-datagovtheme and its requirements..."
cd ckanext-datagovtheme
sudo python setup.py develop

echo "travis-build.bash is done."

echo "TESTING ckanext-datagovtheme with CKAN 2.3 and Bootstrap 2"
sudo -H python -m pip install -r dev-requirements.txt
nosetests --ckan --with-pylons=test-catalog-2.3.ini ckanext/datagovtheme/tests --nologcapture