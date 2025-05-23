import urllib.parse
import ckan.plugins as p
from ckan.plugins.toolkit import config
from ckan.lib.base import abort
from ckan.common import c, request

from flask import Blueprint, redirect, session

import logging
log = logging.getLogger(__name__)

pusher = Blueprint('datagovtheme', __name__)


def show():
    # TODO rename config option to ckanext.datagovtheme
    viewer_url = config.get('ckanext.geodatagov.spatial_preview.url')

    if not viewer_url:
        abort(500, 'Viewer URL not defined')

    params_to_forward = {}
    viewer_params = ['url', 'servicetype', 'srs']

    for key, value in request.params.items():
        if key.lower() in viewer_params:
            params_to_forward[key] = value

    params_to_forward['mode'] = 'advanced'

    c.viewer_url = '{0}?{1}'.format(viewer_url.strip('?'), urllib.parse.urlencode(params_to_forward))

    return p.toolkit.render('viewer.html')


def redirect_homepage():
    CKAN_SITE_URL = config.get("ckan.site_url")
    return redirect(CKAN_SITE_URL + "/dataset/", code=302)


pusher.add_url_rule('/', view_func=redirect_homepage)


@pusher.before_app_request
def refresh_session():
    """ Refresh session expiration time on each request """
    session.modified = True
