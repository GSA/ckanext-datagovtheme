import urllib.parse
import ckan.plugins as p
from ckan.plugins.toolkit import config
from ckan.lib.base import abort
from ckan.common import c, request
from ckanext.datagovtheme import helpers

from flask import Blueprint, redirect, jsonify

import logging
log = logging.getLogger(__name__)

datagovtheme_bp = Blueprint('datagovtheme', __name__)


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


def get_popuplar_count():
    pkgs = request.args.get('pkgs')
    return jsonify(helpers.get_pkgs_popular_count(pkgs))


datagovtheme_bp.add_url_rule('/', view_func=redirect_homepage)
datagovtheme_bp.add_url_rule("/datagovtheme/get-popular-count",
                             methods=['GET'],
                             view_func=get_popuplar_count)
