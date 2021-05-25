#!/bin/bash
# Setup and run extension tests. This script should be run in a _clean_ CKAN
# environment. e.g.:
#
#     $ docker-compose run --rm app ./test.sh
#

set -o errexit
set -o pipefail

# configure environment for tests
export CKAN_SQLALCHEMY_URL=postgresql://ckan_default:pass@db/ckan_test
export CKAN_DATASTORE_WRITE_URL=postgresql://datastore_write:pass@db/datastore_test
export CKAN_DATASTORE_READ_URL=postgresql://datastore_read:pass@db/datastore_test
export CKAN_SOLR_URL=http://solr:8983/solr/ckan
export CKAN_REDIS_URL=redis://redis:6379/1

# Wrapper for paster/ckan.
# CKAN 2.9 replaces paster with ckan CLI. This wrapper abstracts which comand
# is called.
#
# In order to keep the parsing simple, the first argument MUST be
# --plugin=plugin-name. The config option -c is assumed to be
# test.ini because the argument ordering matters to paster and
# ckan, and again, we want to keep the parsing simple.
function ckan_wrapper () {
  if command -v paster > /dev/null; then
    paster "$@" -c test.ini
  else
    shift  # drop the --plugin= argument
    ckan -c test.ini "$@"
  fi
}

ckan_wrapper --plugin=ckan db init
ckan_wrapper --plugin=ckanext-harvest harvester initdb

pytest --ckan-ini=test.ini --cov=ckanext.datagovtheme --disable-warnings ckanext/datagovtheme/tests
