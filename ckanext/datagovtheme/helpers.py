import copy
import csv
import json
import logging
import os
import re
import urllib.parse
import urllib.request

import pkg_resources

from ckan import plugins as p
from ckan.lib import helpers as h
from ckan import model
from ckanext.harvest.model import HarvestObject
from ckan.plugins.toolkit import asbool

from ckan.plugins.toolkit import config

log = logging.getLogger(__name__)

# TODO figure out where this belongs
# This is used in multiple extensions, including ckanext-geodatagov. It seems
# like it's just data and could be exposed differently. We could also provide a
# fallback, so if ckanext-geodatagov is available, use the data from that,
# otherwise fallback to an alternative.
RESOURCE_MAPPING = {
    # ArcGIS File Types
    'esri rest': ('Esri REST', 'Esri REST API Endpoint'),
    'arcgis_rest': ('Esri REST', 'Esri REST API Endpoint'),
    'web map application': ('ArcGIS Online Map', 'ArcGIS Online Map'),
    'arcgis map preview': ('ArcGIS Map Preview', 'ArcGIS Map Preview'),
    'arcgis map service': ('ArcGIS Map Service', 'ArcGIS Map Service'),
    'wms': ('WMS', 'ArcGIS Web Mapping Service'),
    'wfs': ('WFS', 'ArcGIS Web Feature Service'),
    'wcs': ('WCS', 'Web Coverage Service'),

    # CSS File Types
    'css': ('CSS', 'Cascading Style Sheet File'),
    'text/css': ('CSS', 'Cascading Style Sheet File'),

    # CSV File Types
    'csv': ('CSV', 'Comma Separated Values File'),
    'text/csv': ('CSV', 'Comma Separated Values File'),

    # EXE File Types
    'exe': ('EXE', 'Windows Executable Program'),
    'application/x-msdos-program': ('EXE', 'Windows Executable Program'),

    # HyperText Markup Language (HTML) File Types
    'htx': ('HTML', 'Web Page'),
    'htm': ('HTML', 'Web Page'),
    'html': ('HTML', 'Web Page'),
    'htmls': ('HTML', 'Web Page'),
    'xhtml': ('HTML', 'Web Page'),
    'text/html': ('HTML', 'Web Page'),
    'application/xhtml+xml': ('HTML', 'Web Page'),
    'application/x-httpd-php': ('HTML', 'Web Page'),

    # Image File Types - BITMAP
    'bm': ('BMP', 'Bitmap Image File'),
    'bmp': ('BMP', 'Bitmap Image File'),
    'pbm': ('BMP', 'Bitmap Image File'),
    'xbm': ('BMP', 'Bitmap Image File'),
    'image/bmp': ('BMP', 'Bitmap Image File'),
    'image/x-ms-bmp': ('BMP', 'Bitmap Image File'),
    'image/x-xbitmap': ('BMP', 'Bitmap Image File'),
    'image/x-windows-bmp': ('BMP', 'Bitmap Image File'),
    'image/x-portable-bitmap': ('BMP', 'Bitmap Image File'),

    # Image File Types - Graphics Interchange Format (GIF)
    'gif': ('GIF', 'GIF Image File'),
    'image/gif': ('GIF', 'GIF Image File'),

    # Image File Types - ICON
    'ico': ('ICO', 'Icon Image File'),
    'image/x-icon': ('ICO', 'Icon Image File'),

    # Image File Types - JPEG
    'jpe': ('JPEG', 'JPEG Image File'),
    'jpg': ('JPEG', 'JPEG Image File'),
    'jps': ('JPEG', 'JPEG Image File'),
    'jpeg': ('JPEG', 'JPEG Image File'),
    'pjpeg': ('JPEG', 'JPEG Image File'),
    'image/jpeg': ('JPEG', 'JPEG Image File'),
    'image/pjpeg': ('JPEG', 'JPEG Image File'),
    'image/x-jps': ('JPEG', 'JPEG Image File'),
    'image/x-citrix-jpeg': ('JPEG', 'JPEG Image File'),

    # Image File Types - PNG
    'png': ('PNG', 'PNG Image File'),
    'x-png': ('PNG', 'PNG Image File'),
    'image/png': ('PNG', 'PNG Image File'),
    'image/x-citrix-png': ('PNG', 'PNG Image File'),

    # Image File Types - Scalable Vector Graphics (SVG)
    'svg': ('SVG', 'SVG Image File'),
    'image/svg+xml': ('SVG', 'SVG Image File'),

    # Image File Types - Tagged Image File Format (TIFF)
    'tif': ('TIFF', 'TIFF Image File'),
    'tiff': ('TIFF', 'TIFF Image File'),
    'image/tiff': ('TIFF', 'TIFF Image File'),
    'image/x-tiff': ('TIFF', 'TIFF Image File'),

    # JSON File Types
    'json': ('JSON', 'JSON File'),
    'text/x-json': ('JSON', 'JSON File'),
    'application/json': ('JSON', 'JSON File'),

    # KML File Types
    'kml': ('KML', 'KML File'),
    'kmz': ('KML', 'KMZ File'),
    'application/vnd.google-earth.kml+xml': ('KML', 'KML File'),
    'application/vnd.google-earth.kmz': ('KML', 'KMZ File'),

    # MS Access File Types
    'mdb': ('ACCESS', 'MS Access Database'),
    'access': ('ACCESS', 'MS Access Database'),
    'application/mdb': ('ACCESS', 'MS Access Database'),
    'application/msaccess': ('ACCESS', 'MS Access Database'),
    'application/x-msaccess': ('ACCESS', 'MS Access Database'),
    'application/vnd.msaccess': ('ACCESS', 'MS Access Database'),
    'application/vnd.ms-access': ('ACCESS', 'MS Access Database'),

    # MS Excel File Types
    'xl': ('EXCEL', 'MS Excel File'),
    'xla': ('EXCEL', 'MS Excel File'),
    'xlb': ('EXCEL', 'MS Excel File'),
    'xlc': ('EXCEL', 'MS Excel File'),
    'xld': ('EXCEL', 'MS Excel File'),
    'xls': ('EXCEL', 'MS Excel File'),
    'xlsx': ('EXCEL', 'MS Excel File'),
    'xlsm': ('EXCEL', 'MS Excel File'),
    'excel': ('EXCEL', 'MS Excel File'),
    'openXML': ('EXCEL', 'MS Excel File'),
    'application/excel': ('EXCEL', 'MS Excel File'),
    'application/x-excel': ('EXCEL', 'MS Excel File'),
    'application/x-msexcel': ('EXCEL', 'MS Excel File'),
    'application/vnd.ms-excel': ('EXCEL', 'MS Excel File'),
    'application/vnd.ms-excel.sheet.macroEnabled.12': ('EXCEL', 'MS Excel File'),
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ('EXCEL', 'MS Excel File'),

    # MS PowerPoint File Types
    'ppt': ('POWERPOINT', 'MS PowerPoint File'),
    'pps': ('POWERPOINT', 'MS PowerPoint File'),
    'pptx': ('POWERPOINT', 'MS PowerPoint File'),
    'ppsx': ('POWERPOINT', 'MS PowerPoint File'),
    'pptm': ('POWERPOINT', 'MS PowerPoint File'),
    'ppsm': ('POWERPOINT', 'MS PowerPoint File'),
    'sldx': ('POWERPOINT', 'MS PowerPoint File'),
    'sldm': ('POWERPOINT', 'MS PowerPoint File'),
    'application/powerpoint': ('POWERPOINT', 'MS PowerPoint File'),
    'application/mspowerpoint': ('POWERPOINT', 'MS PowerPoint File'),
    'application/x-mspowerpoint': ('POWERPOINT', 'MS PowerPoint File'),
    'application/vnd.ms-powerpoint': ('POWERPOINT', 'MS PowerPoint File'),
    'application/vnd.ms-powerpoint.presentation.macroEnabled.12': ('POWERPOINT', 'MS PowerPoint File'),
    'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': ('POWERPOINT', 'MS PowerPoint File'),
    'application/vnd.ms-powerpoint.slide.macroEnabled.12': ('POWERPOINT', 'MS PowerPoint File'),
    'application/vnd.openxmlformats-officedocument.presentationml.slide': ('POWERPOINT', 'MS PowerPoint File'),
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': ('POWERPOINT', 'MS PowerPoint File'),
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': ('POWERPOINT', 'MS PowerPoint File'),

    # MS Word File Types
    'doc': ('DOC', 'MS Word File'),
    'docx': ('DOC', 'MS Word File'),
    'docm': ('DOC', 'MS Word File'),
    'word': ('DOC', 'MS Word File'),
    'application/msword': ('DOC', 'MS Word File'),
    'application/vnd.ms-word.document.macroEnabled.12': ('DOC', 'MS Word File'),
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ('DOC', 'MS Word File'),

    # Network Common Data Form (NetCDF) File Types
    'nc': ('CDF', 'NetCDF File'),
    'cdf': ('CDF', 'NetCDF File'),
    'netcdf': ('CDF', 'NetCDF File'),
    'application/x-netcdf': ('NETCDF', 'NetCDF File'),

    # PDF File Types
    'pdf': ('PDF', 'PDF File'),
    'application/pdf': ('PDF', 'PDF File'),

    # PERL File Types
    'pl': ('PERL', 'Perl Script File'),
    'pm': ('PERL', 'Perl Module File'),
    'perl': ('PERL', 'Perl Script File'),
    'text/x-perl': ('PERL', 'Perl Script File'),

    # QGIS File Types
    'qgis': ('QGIS', 'QGIS File'),
    'application/x-qgis': ('QGIS', 'QGIS File'),

    # RAR File Types
    'rar': ('RAR', 'RAR Compressed File'),
    'application/rar': ('RAR', 'RAR Compressed File'),
    'application/vnd.rar': ('RAR', 'RAR Compressed File'),
    'application/x-rar-compressed': ('RAR', 'RAR Compressed File'),

    # Resource Description Framework (RDF) File Types
    'rdf': ('RDF', 'RDF File'),
    'application/rdf+xml': ('RDF', 'RDF File'),

    # Rich Text Format (RTF) File Types
    'rt': ('RICH TEXT', 'Rich Text File'),
    'rtf': ('RICH TEXT', 'Rich Text File'),
    'rtx': ('RICH TEXT', 'Rich Text File'),
    'text/richtext': ('RICH TEXT', 'Rich Text File'),
    'text/vnd.rn-realtext': ('RICH TEXT', 'Rich Text File'),
    'application/rtf': ('RICH TEXT', 'Rich Text File'),
    'application/x-rtf': ('RICH TEXT', 'Rich Text File'),

    # SID File Types - Primary association: Commodore64 (C64)?
    'sid': ('SID', 'SID File'),
    'mrsid': ('SID', 'SID File'),
    'audio/psid': ('SID', 'SID File'),
    'audio/x-psid': ('SID', 'SID File'),
    'audio/sidtune': ('SID', 'MID File'),
    'audio/x-sidtune': ('SID', 'SID File'),
    'audio/prs.sid': ('SID', 'SID File'),

    # Tab Separated Values (TSV) File Types
    'tsv': ('TSV', 'Tab Separated Values File'),
    'text/tab-separated-values': ('TSV', 'Tab Separated Values File'),

    # Tape Archive (TAR) File Types
    'tar': ('TAR', 'TAR Compressed File'),
    'application/x-tar': ('TAR', 'TAR Compressed File'),

    # Text File Types
    'txt': ('TEXT', 'Text File'),
    'text/plain': ('TEXT', 'Text File'),

    # Extensible Markup Language (XML) File Types
    'xml': ('XML', 'XML File'),
    'text/xml': ('XML', 'XML File'),
    'application/xml': ('XML', 'XML File'),

    # XYZ File Format File Types
    'xyz': ('XYZ', 'XYZ File'),
    'chemical/x-xyz': ('XYZ', 'XYZ File'),

    # ZIP File Types
    'zip': ('ZIP', 'Zip File'),
    'application/zip': ('ZIP', 'Zip File'),
    'multipart/x-zip': ('ZIP', 'Zip File'),
    'application/x-compressed': ('ZIP', 'Zip File'),
    'application/x-zip-compressed': ('ZIP', 'Zip File'),
}


def api_doc_url():
    lang = h.lang()
    ckan_major_minor_version = '.'.join(h.ckan_version().split('.')[0:2])

    return 'https://docs.ckan.org/{lang}/{version}/api/index.html'.format(
           lang=lang, version=ckan_major_minor_version)


def render_datetime_datagov(date_str):
    try:
        value = h.render_datetime(date_str)
    except (ValueError, TypeError):
        return date_str
    return value


def get_harvest_object_formats(harvest_object_id):
    try:
        obj = p.toolkit.get_action('harvest_object_show')({}, {'id': harvest_object_id})
    except p.toolkit.ObjectNotFound:
        log.info('Harvest object not found {0}:'.format(harvest_object_id))
        return {}

    def get_extra(obj, key, default=None):
        for k, v in obj['extras'].items():
            if k == key:
                return v
        return default

    def format_title(format_name):
        format_titles = {
            'iso': 'ISO-19139',
            'fgdc': 'FGDC',
            'arcgis_json': 'ArcGIS JSON',
            'ckan': 'CKAN'
        }
        return format_titles[format_name] if format_name in format_titles else format_name

    def format_type(format_name):
        if not format_name:
            return ''

        if format_name in ('iso', 'fgdc'):
            format_type = 'xml'
        elif format_name in ('arcgis'):
            format_type = 'json'
        elif format_name in ('ckan'):
            format_type = 'ckan'
        else:
            format_type = ''
        return format_type

    format_name = get_extra(obj, 'format', 'iso')
    original_format_name = get_extra(obj, 'original_format')

    # check if harvest_object holds a ckan_url key
    try:
        json.loads(obj['content'])['ckan_url']
        format_name = 'ckan'
    except Exception:
        pass

    return {
        'object_format': format_title(format_name),
        'object_format_type': format_type(format_name),
        'original_format': format_title(original_format_name),
        'original_format_type': format_type(original_format_name),
    }


def get_harvest_source_link(package_dict):
    harvest_source_id = get_pkg_dict_extra(package_dict, 'harvest_source_id', None)
    harvest_source_title = get_pkg_dict_extra(package_dict, 'harvest_source_title', None)

    if harvest_source_id and harvest_source_title:
        msg = p.toolkit._('Harvested from')
        url = h.url_for('harvest_read', id=harvest_source_id)
        link = '{msg} <a href="{url}">{title}</a>'.format(url=url, msg=msg, title=harvest_source_title)
        return p.toolkit.literal(link)

    return ''


# https://github.com/ckan/ckanext-spatial/blob/011008b9c5c4bf58ddd401c805328a9928bbe4ea/ckanext/spatial/helpers.py
def get_reference_date(date_str):
    '''
        Gets a reference date extra created by the harvesters and formats it
        nicely for the UI.
        Examples:
            [{"type": "creation", "value": "1977"}, {"type": "revision", "value": "1981-05-15"}]
            [{"type": "publication", "value": "1977"}]
            [{"type": "publication", "value": "NaN-NaN-NaN"}]
        Results
            1977 (creation), May 15, 1981 (revision)
            1977 (publication)
            NaN-NaN-NaN (publication)
    '''
    try:
        out = []
        for date in h.json.loads(date_str):
            value = h.render_datetime(date['value']) or date['value']
            out.append('{0} ({1})'.format(value, date['type']))
        return ', '.join(out)
    except (ValueError, TypeError):
        return date_str


# https://github.com/ckan/ckanext-spatial/blob/011008b9c5c4bf58ddd401c805328a9928bbe4ea/ckanext/spatial/helpers.py#L35
# This doesn't seem specific to ckanext-spatial. Maybe this should move into ckanext-harvest or ckan proper?
def get_responsible_party(value):
    '''
        Gets a responsible party extra created by the harvesters and formats it
        nicely for the UI.
        Examples:
            [{"name": "Complex Systems Research Center", "roles": ["pointOfContact"]}]
            [
                {"name": "British Geological Survey", "roles": ["custodian", "pointOfContact"]},
                {"name": "Natural England", "roles": ["publisher"]}
            ]
        Results
            Complex Systems Research Center (pointOfContact)
            British Geological Survey (custodian, pointOfContact); Natural England (publisher)
    '''
    formatted = {
        'resourceProvider': p.toolkit._('Resource Provider'),
        'pointOfContact': p.toolkit._('Point of Contact'),
        'principalInvestigator': p.toolkit._('Principal Investigator'),
    }

    try:
        out = []
        parties = h.json.loads(value)
        for party in parties:
            roles = [formatted[role] if role in list(formatted.keys()) else p.toolkit._(role.capitalize()) for role in
                     party['roles']]
            out.append('{0} ({1})'.format(party['name'], ', '.join(roles)))
        return '; '.join(out)
    except (ValueError, TypeError):
        return value


def is_map_viewer_format(resource):
    # TODO rename config option to ckanext.datagovtheme
    viewer_url = config.get('ckanext.geodatagov.spatial_preview.url')
    viewer_formats = config.get('ckanext.geodatagov.spatial_preview.formats', 'wms kml kmz').strip().split(' ')

    return viewer_url and resource.get('url') and resource.get('format', '').lower() in viewer_formats


def get_map_viewer_params(resource, advanced=False):

    params = {
        'url': resource['url'],
        'serviceType': resource.get('format'),
    }
    if resource.get('default_srs'):
        params['srs'] = resource['default_srs']

    if advanced:
        params['mode'] == 'advanced'

    return urllib.parse.urlencode(params)


types = {
    'web': ('html', 'data', 'esri rest', 'gov', 'org', ''),
    'preview': ('csv', 'xls', 'txt', 'jpg', 'jpeg', 'png', 'gif'),
    # "web map application" is deprecated in favour of "arcgis online map"
    'map': ('wms', 'kml', 'kmz', 'georss', 'web map application', 'arcgis online map'),
    'plotly': ('csv', 'xls', 'excel', 'openxml', 'access', 'application/vnd.ms-excel',
               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
               'text/csv', 'text/tab-separated-values',
               'application/matlab-mattext/x-matlab', 'application/x-msaccess',
               'application/msaccess', 'application/x-hdf', 'application/x-bag'),
    'cartodb': ('csv', 'xls', 'excel', 'openxml', 'kml', 'geojson', 'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'text/csv', 'application/vnd.google-earth.kml+xml',
                'application/vnd.geo+json'),
    'arcgis': ('esri rest', 'wms', 'kml', 'kmz', 'application/vnd.google-earth.kml+xml', 'georss')
}


def is_type_format(type, resource):
    if resource and type in types:
        format = resource.get('format', 'data').lower()
        # TODO: convert mimetypes to formats so we dont have to do this.
        mimetype = resource.get('mimetype')
        if mimetype:
            mimetype = mimetype.lower()
        if format in types[type] or mimetype in types[type]:
            return True
    return False


def is_web_format(resource):
    return is_type_format('web', resource)


def is_preview_format(resource):
    return is_type_format('preview', resource)


def is_map_format(resource):
    return is_type_format('map', resource)


def is_plotly_format(resource):
    return is_type_format('plotly', resource)


def is_cartodb_format(resource):
    return is_type_format('cartodb', resource)


def is_arcgis_format(resource):
    return is_type_format('arcgis', resource)


def arcgis_format_query(resource):
    mimetype = resource.get('mimetype', None)
    kmlstring = re.compile('(kml|kmz)')
    if kmlstring.match(str(mimetype)):
        return 'kml'
    else:
        # wms, georss
        return mimetype


def convert_resource_format(format):
    if format:
        format = format.lower()
    formats = list(RESOURCE_MAPPING.keys())
    if format in formats:
        format = RESOURCE_MAPPING[format][1]
    else:
        format = 'Web Resource'

    return format


def remove_extra_chars(str_value):
    # this will remove brackets for list and dict values.
    import ast
    new_value = None

    try:
        new_value = ast.literal_eval(str_value)
    except Exception:
        pass

    if type(new_value) is list:
        new_value = [i.strip() for i in new_value]
        ret = ', '.join(new_value)
    elif type(new_value) is dict:
        ret = ', '.join('{0}:{1}'.format(key, val) for key, val in list(new_value.items()))
    else:
        ret = str_value

    return ret


def schema11_key_mod(key):
    key_map = {
        'Catalog @Context': 'Metadata Context',
        'Catalog @Id': 'Metadata Catalog ID',
        'Catalog Conformsto': 'Schema Version',
        'Catalog DescribedBy': 'Data Dictionary',

        # 'Identifier': 'Unique Identifier',
        'Modified': 'Data Last Modified',
        'Accesslevel': 'Public Access Level',
        'Bureaucode': 'Bureau Code',
        'Programcode': 'Program Code',
        'Accrualperiodicity': 'Data Update Frequency',
        'Conformsto': 'Data Standard',
        'Dataquality': 'Data Quality',
        'Describedby': 'Data Dictionary',
        'Describedbytype': 'Data Dictionary Type',
        'Issued': 'Data First Published',
        'Landingpage': 'Homepage URL',
        'Primaryitinvestmentuii': 'Primary IT Investment UII',
        'References': 'Related Documents',
        'Systemofrecords': 'System of Records',
        'Theme': 'Category',
    }

    return key_map.get(key, key)


def schema11_frequency_mod(value):
    frequency_map = {
        'R/P10Y': 'Decennial',
        'R/P4Y': 'Quadrennial',
        'R/P1Y': 'Annual',
        'R/P2M': 'Bimonthly',
        'R/P0.5M': 'Bimonthly',
        'R/P3.5D': 'Semiweekly',
        'R/P1D': 'Daily',
        'R/P2W': 'Biweekly',
        'R/P0.5W': 'Biweekly',
        'R/P6M': 'Semiannual',
        'R/P2Y': 'Biennial',
        'R/P3Y': 'Triennial',
        'R/P0.33W': 'Three times a week',
        'R/P0.33M': 'Three times a month',
        'R/PT1S': 'Continuously updated',
        'R/P1M': 'Monthly',
        'R/P3M': 'Quarterly',
        'R/P4M': 'Three times a year',
        'R/P1W': 'Weekly',
    }
    return frequency_map.get(value, value)


def convert_top_category_to_list(str_value):
    import ast
    list_value = None

    try:
        list_value = ast.literal_eval(str_value)
    except Exception:
        pass

    if type(list_value) is not list:
        list_value = []

    return list_value


def get_bureau_info(bureau_code):
    """
    Maps Bureau Codes to a title, logo, and dataset URL.

    bureau_code: bureau code string or a list of bureau code strings.

    returns dict(title, url, code, logo) or None if there was an error or the bureau code does not exist in our list.
    """

    if not bureau_code:
        return None

    WEB_PATH = '/images/logos/'
    LOCAL_PATH = 'fanstatic_library/images/logos/'

    # handle both '007:15', or ['007:15', '007:16']
    if isinstance(bureau_code, list):
        bureau_code = bureau_code[0]

    try:
        agency_part, bureau_part = bureau_code.split(':')
    except ValueError:
        log.warning('bureau code is invalid code=%s' % bureau_code)
        return None

    controller = 'dataset'

    # TODO in python 3, replace pkg_resources with [importlib-resources](https://pypi.org/project/importlib-resources/)
    bureau_filename = pkg_resources.resource_filename('ckanext.datagovtheme.data', 'omb_bureau_codes.csv')

    # Python 3 csv.reader wants text data
    bureau_file = open(bureau_filename, 'r', newline='', encoding='utf8')

    # Should this be cached in memory as an index to speed things up?
    bureau_table = csv.reader(bureau_file)
    for row in bureau_table:
        # We're doing the zfill to pad for 000 every lookup, more reason to
        # cache this or do a transform when the file is imported into the
        # repository.
        if agency_part == row[2].zfill(3) and bureau_part == row[3].zfill(2):
            bureau_title = row[1]
            bureau_url = h.url_for(controller=controller, action='search', q='bureauCode:"%s"' % bureau_code)
            break
    else:
        log.warning('omb_bureau_codes.csv is empty')
        return None

    # TODO in python 3, use a context manager since we won't need the conditional `open`
    bureau_file.close()

    # check logo image file exists or not
    # should this be cached as in index to speed this up?
    bureau_logo = None
    for ext in ['png', 'gif', 'jpg']:
        logo_filename = '%s-%s.%s' % (agency_part, bureau_part, ext)
        # We should probably be using pre_resources here, too, but we also need
        # to add the logos as assets. That seems to be magically working right
        # now?
        if os.path.isfile(os.path.join(os.path.dirname(__file__), LOCAL_PATH) + logo_filename):
            bureau_logo = h.url_for_static(WEB_PATH + logo_filename)
            break

    return {
        'title': bureau_title,
        'code': bureau_code,
        'logo': bureau_logo,
        'url': bureau_url,
    }


# returns true if the package contains a tag with the name 'ngda
def is_tagged_ngda(pkg_dict):
    if 'tags' in pkg_dict:
        for tag in pkg_dict['tags']:
            if tag['name'].lower() == 'ngda':
                return True
    return False


# TODO can we drop this dependency on ckanext-harvest? Can this be moved to ckanext-harvest? geodatagov?
def get_pkg_dict_extra(pkg_dict, key, default=None):
    '''Override the CKAN core helper to add rolled up extras
    Returns the value for the dataset extra with the provided key.

    If the key is not found, it returns a default value, which is None by
    default.

    :param pkg_dict: dictized dataset
    :key: extra key to lookup
    :default: default value returned if not found
    '''
    extras = pkg_dict['extras'] if 'extras' in pkg_dict else []

    for extra in extras:
        if extra['key'] == key:
            return extra['value']

    # also include the rolled up extras
    for extra in extras:
        if 'extras_rollup' == extra.get('key'):
            rolledup_extras = json.loads(extra.get('value'))
            for k, value in rolledup_extras.items():
                if k == key:
                    return value

    # Also include harvest information if exists
    if key in ['harvest_object_id', 'harvest_source_id', 'harvest_source_title']:

        harvest_object = model.Session.query(HarvestObject) \
                .filter(HarvestObject.package_id == pkg_dict['id']) \
                .filter(HarvestObject.current == True).first()  # noqa

        if harvest_object:
            if key == 'harvest_object_id':
                return harvest_object.id
            elif key == 'harvest_source_id':
                return harvest_object.source.id
            elif key == 'harvest_source_title':
                return harvest_object.source.title

    return default

# from GSA/ckanext-archiver


def archiver_resource_info_table(resource):
    archival = resource.get('archiver')
    if not archival:
        return p.toolkit.literal('<!-- No archival info for this resource -->')
    extra_vars = {'resource': resource}
    extra_vars.update(archival)
    res = p.toolkit.literal(
        p.toolkit.render('archiver/resource_info_table.html',
                         extra_vars=extra_vars)
    )
    return res


def archiver_is_resource_broken_line(resource):
    archival = resource.get('archiver')
    if not archival:
        return p.toolkit.literal('<!-- No archival info for this resource -->')
    extra_vars = {'resource': resource}
    extra_vars.update(archival)
    res = p.toolkit.literal(
        p.toolkit.render('archiver/is_resource_broken_line.html',
                         extra_vars=extra_vars))
    return res

# from GSA/ckanext-qa


def qa_openness_stars_resource_line(resource):
    qa = resource.get('qa')
    if not qa:
        return p.toolkit.literal('<!-- No qa info for this resource -->')
    if not isinstance(qa, dict):
        return p.toolkit.literal('<!-- QA info was of the wrong type -->')
    extra_vars = copy.deepcopy(qa)
    return p.toolkit.literal(
        p.toolkit.render('qa/openness_stars_line.html',
                         extra_vars=extra_vars))


def qa_openness_stars_resource_table(resource):
    qa = resource.get('qa')
    if not qa:
        return p.toolkit.literal('<!-- No qa info for this resource -->')
    if not isinstance(qa, dict):
        return p.toolkit.literal('<!-- QA info was of the wrong type -->')
    extra_vars = copy.deepcopy(qa)
    return p.toolkit.literal(
        p.toolkit.render('qa/openness_stars_table.html',
                         extra_vars=extra_vars))


def get_login_url():
    # TODO maybe make this a configuration option for ckanext.saml2auth instead of the implicit dependency
    # TODO push this upstream to ckanext.saml2auth, we should be able to use url_for
    # TODO if we have to rely on a config option, it should be in the ckanext.datagovtheme namespace
    enable_ckan_internal_login = asbool(config.get('ckanext.saml2auth.enable_ckan_internal_login', 'true'))
    if enable_ckan_internal_login:
        return h.url_for(controller='user', action='login')

    return '/user/saml2login'
