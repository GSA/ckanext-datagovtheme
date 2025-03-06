ARG CKAN_VERSION=2.11.2
FROM ckan/ckan-dev:${CKAN_VERSION}
ARG CKAN_VERSION

USER root

RUN apt-get update && apt-get install -y libgeos-dev

COPY . $APP_DIR/

RUN pip install -r $APP_DIR/requirements.txt -r $APP_DIR/dev-requirements.txt -e $APP_DIR/.
