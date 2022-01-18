ARG CKAN_VERSION=2.9
FROM openknowledge/ckan-dev:${CKAN_VERSION}
ARG CKAN_VERSION

# Add timezone data if it does not exist
RUN if [[ "${CKAN_VERSION}" = "2.9" ]]; then sudo apk add tzdata; fi

COPY . $APP_DIR/
# WORKDIR /app

RUN pip install -r $APP_DIR/requirements.txt -r $APP_DIR/dev-requirements.txt -e $APP_DIR/.
