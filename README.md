# ckanext-datagovtheme

[![Github Actions](https://github.com/GSA/ckanext-datagovtheme/actions/workflows/ckan.yml/badge.svg)](https://github.com/GSA/ckanext-datagovtheme/actions)
[![PyPI version](https://badge.fury.io/py/ckanext-datagovtheme.svg)](https://badge.fury.io/py/ckanext-datagovtheme)

Data.gov theme, branding, and UI customizations for
[catalog.data.gov](https://catalog.data.gov/) as a [CKAN](https://ckan.org/)
extension.


## Features

_TODO document these better._

- Provides a new spatial query view (overrides [ckanext-spatial](https://github.com/ckan/ckanext-spatial) some front end)


## Usage


### Requirements

_TODO: document how ckanext-datagovtheme interacts with third-party extensions, maybe
in the context of Features above._

These extensions are required.

- [ckanext-spatial](https://github.com/gsa/ckanext-spatial)
- [ckanext-harvest](https://github.com/ckan/ckanext-harvest)

Additionally, ckanext-datagovtheme has "weak" dependencies on these extensions.
The dependency might be on templates, template helpers, or other functionality.

- [ckanext-archiver](https://github.com/ckan/ckanext-archiver)
- [ckanext-dcat](https://github.com/ckan/ckanext-dcat)
- [ckanext-qa](https://github.com/ckan/ckanext-qa)

This extension is compatible with these versions of CKAN.

CKAN version | Compatibility
------------ | -------------
<=2.8        | no
2.9          | 0.1.27 (last supported)
2.10         | >=0.2.0


### Configuration

_TODO: what configuraiton options exist?_


## Development

### Requirements

- GNU Make
- Docker Compose


### Setup

Build the docker containers. You'll want to do this anytime the dependencies
change (requirements.txt, dev-requirements.txt).

    $ make build

Start the containers.

    $ make up

CKAN will start at [localhost:5000](http://localhost:5000).

Clean up the environment.

    $ make down

Open a shell to run commands in the container.

    $ docker-compose exec ckan bash

If you're unfamiliar with docker-compose, see our
[cheatsheet](https://github.com/GSA/datagov-deploy/wiki/Docker-Best-Practices#cheatsheet)
and the [official docs](https://docs.docker.com/compose/reference/).

For additional make targets, see the help.

    $ make help


### Testing

They follow the guidelines for [testing CKAN extensions](https://docs.ckan.org/en/2.8/extensions/testing-extensions.html#testing-extensions).

To run the extension tests:

    $ make test

Lint your code.

    $ make lint

#### Common issues

We have seen issues with `datagovtheme not installed`.
If this is the case, run `python setup.py develop` in the container.

### Matrix builds

The development environment drops as many dependencies as possible. It is
not meant to have feature parity with
[GSA/catalog.data.gov](https://github.com/GSA/catalog.data.gov/) or
[GSA/inventory-app](https://github.com/GSA/inventory-app/). Tests should mock
external dependencies where possible.

In order to support multiple versions of CKAN, or even upgrade to new versions
of CKAN, we support development and testing through the `CKAN_VERSION`
environment variable.

    $ make CKAN_VERSION=2.10 test


Variable | Description | Default
-------- | ----------- | -------
CKAN_VERSION | Version of CKAN to use. | 2.10
COMPOSE_FILE | docker-compose service description file. | docker-compose.yml
