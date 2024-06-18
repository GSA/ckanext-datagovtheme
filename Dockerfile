ARG CKAN_VERSION=2.10.1
FROM ckan/ckan-dev:${CKAN_VERSION}
ARG CKAN_VERSION

# add sudo
RUN set -ex && apk --no-cache add sudo

# Add timezone data
RUN sudo apk add tzdata proj-util proj-dev geos-dev

COPY . $APP_DIR/

RUN pip install -r $APP_DIR/requirements.txt -r $APP_DIR/dev-requirements.txt -e $APP_DIR/.
