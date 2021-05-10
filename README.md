# ckanext-datagovtheme

[![CircleCI](https://circleci.com/gh/GSA/ckanext-datagovtheme.svg?style=svg)](https://circleci.com/gh/GSA/ckanext-datagovtheme)

Data.gov theme, branding, and UI customizations for
[catalog.data.gov](https://catalog.data.gov/) as a [CKAN](https://ckan.org/)
extension.


## Usage


### Requirements

_TODO: document how ckanext-datagovtheme interacts with third-party extensions._

These extensions are required.

- [ckanext-geodatagov](https://github.com/GSA/ckanext-geodatagov)
- [ckanext-spatial](https://github.com/ckan/ckanext-spatial)

Additionally, ckanext-datagovtheme has "weak" dependencies on these extensions.
The dependency might be on templates, template helpers, or other functionality.

- [ckanext-archiver](https://github.com/ckan/ckanext-archiver)
- [ckanext-qa](https://github.com/ckan/ckanext-qa)

This extension is compatible with these versions of CKAN.

CKAN version | Compatibility
------------ | -------------
<=2.7        | no
2.8          | yes
2.9          | in progress


### Configuration

_TODO: what configuraiton options exist?_


## Development

### Requirements

- GNU Make
- Docker Compose


### Setup

Build the docker containers.

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

To run the extension tests, start the containers with `make up`, then:

    $ make test

Lint your code.

    $ make lint
