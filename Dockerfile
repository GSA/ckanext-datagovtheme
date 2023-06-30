ARG CKAN_VERSION=2.10.1
FROM openknowledge/ckan-dev:${CKAN_VERSION}
ARG CKAN_VERSION

# Add timezone data
RUN sudo apk add tzdata

COPY . $APP_DIR/

RUN pip install -r $APP_DIR/requirements.txt -r $APP_DIR/dev-requirements.txt -e $APP_DIR/.
