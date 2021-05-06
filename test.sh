#!/bin/bash
# Setup and run extension tests. This script should be run in a _clean_ CKAN
# environment. e.g.:
#
#     $ docker-compose run --rm app ./test.sh
#

set -o errexit
set -o pipefail



# Wrapper for paster/ckan.
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

pytest --ckan-ini=test.ini --cov=ckanext.datagovtheme --cov-fail-under=40 --disable-warnings ckanext/datagovtheme/tests
