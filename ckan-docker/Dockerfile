FROM openknowledge/ckan-dev:2.8

MAINTAINER Your Name Here <you@example.com>

# Install any extensions needed by your CKAN instance
# (Make sure to add the plugins to CKAN__PLUGINS in the .env file)
# For instance:
RUN pip install -e git+https://github.com/ckan/ckanext-spatial#egg=ckanext-spatial && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-spatial/master/pip-requirements.txt && \
    pip install -e git+https://github.com/ckan/ckanext-harvest.git#egg=ckanext-harvest && \
    pip install -r https://raw.githubusercontent.com/ckan/ckanext-harvest/master/pip-requirements.txt && \
    pip install -e git+https://github.com/GSA/ckanext-datajson.git#egg=ckanext-datajson && \
    pip install -r https://raw.githubusercontent.com/GSA/ckanext-datajson/master/pip-requirements.txt && \
    pip install -e git+https://github.com/GSA/ckanext-geodatagov.git#egg=ckanext-geodatagov && \
    pip install -r https://raw.githubusercontent.com/GSA/ckanext-geodatagov/master/pip-requirements.txt

# Clone the extension(s) your are writing for your own project in the `src` folder
# to get them mounted in this image at runtime

# Apply any patches needed to CKAN core or any of the built extensions (not the
# runtime mounted ones)