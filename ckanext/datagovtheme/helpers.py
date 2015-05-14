import urllib, urllib2, json, re, HTMLParser, urlparse
import os, time
import logging

from pylons import config, request

from ckan import plugins as p
from ckan.lib import helpers as h

log = logging.getLogger(__name__)

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
        for k, v in obj['extras'].iteritems():
            if k == key:
                return v
        return default

    def format_title(format_name):
        format_titles = {
            'iso': 'ISO-19139',
            'fgdc': 'FGDC',
            'arcgis_json': 'ArcGIS JSON'
        }
        return format_titles[format_name] if format_name in format_titles else format_name

    def format_type(format_name):
        if not format_name:
            return ''

        if format_name in ('iso', 'fgdc'):
            format_type = 'xml'
        elif format_name in ('arcgis'):
            format_type = 'json'
        else:
            format_type = ''
        return format_type

    format_name = get_extra(obj, 'format', 'iso')
    original_format_name = get_extra(obj, 'original_format')

    return {
            'object_format': format_title(format_name),
            'object_format_type': format_type(format_name),
            'original_format': format_title(original_format_name),
            'original_format_type': format_type(original_format_name),
           }

def get_dynamic_menu():
    filename = os.path.join(os.path.dirname(__file__), 'dynamic_menu/menu.json')
    url = config.get('ckanext.geodatagov.dynamic_menu.url', '')
    if not url:
        url = config.get('ckanext.geodatagov.dynamic_menu.url_default', '')

    time_file = 0
    time_current = time.time()
    try:
        time_file = os.path.getmtime(filename)
    except:
        pass

    # check to see if file is older than .5 hour
    if (time_current - time_file) < 3600/2:
        file_obj = open(filename)
        file_conent = file_obj.read()
    else:
        # it means file is old, or does not exist
        # fetch new content
        if os.path.exists(filename):
            sec_timeout = 5
        else:
            sec_timeout = 20 # longer urlopen timeout if there is no backup file.

        try:
            resource = urllib2.urlopen(url, timeout=sec_timeout)
        except:
            file_obj = open(filename)
            file_conent = file_obj.read()
            # touch the file, so that it wont keep re-trying and slow down page loading
            os.utime(filename, None)
        else:
            file_obj = open(filename, 'w+')
            file_conent = resource.read()
            file_obj.write(file_conent)

    file_obj.close()
    # remove jsonp wrapper "jsonCallback(JSON);"
    re_obj = re.compile(r"^jsonCallback\((.*)\);$", re.DOTALL)
    json_menu = re_obj.sub(r"\1", file_conent)
    # unescape &amp; or alike
    html_parser =  HTMLParser.HTMLParser()
    json_menu_clean = None
    try:
        json_menu_clean = html_parser.unescape(json_menu)
    except:
        pass

    menus = ''
    if json_menu_clean:
        try:
            menus = json.loads(json_menu_clean)
        except:
            pass

    query = request.environ.get('QUERY_STRING', '');
    submenu_key = None
    category_1 = None
    category_2 = None
    category = None
    climate_generic_category = None

    if menus and query:
        query_dict = urlparse.parse_qs(query)
        organization_types = query_dict.get('organization_type', [])
        organizations = query_dict.get('organization', [])
        groups = query_dict.get('groups', [])
        if (not groups or groups == ['local']) and organization_types in [
                    ['State Government'],
                    ['City Government'],
                    ['County Government'],
                    ['Local Government'],
                ]:
            # State/County/Cities and Local are merged into 'local' group.
            organization_types = []
            groups = ['local']
        # the three are exclusive
        if sorted([not not organization_types, not not organizations, not not groups]) == [False, False, True]:
            _keys = organization_types or organizations or groups
            if len(_keys) == 1:
                submenu_key = _keys[0]
                if groups:
                    # remove trailing numerics
                    submenu_key = re.sub(r'\d+$', '', submenu_key)
                    submenu_key = submenu_key.lower()

                    categories = query_dict.get('vocab_category_all', [])
                    # some special topic categories got their own sub menus.
                    if submenu_key == 'climate' and categories:
                        cat_food_list = ['Food Resilience', 'Food Production', 'Food Distribution', 'Food Safety and Nutrition', 'Food Security']
                        cat_coastal_list = ['Coastal Flooding']
                        if set(cat_food_list).issuperset(categories):
                            category = 'foodresilience'
                        elif set(cat_coastal_list).issuperset(categories):
                            category = 'coastalflooding'
                        else:
                            # climate special treatment
                            # try replace space with '-' and '', which ever works
                            climate_generic_category = categories[0]
                            category_1 = climate_generic_category.replace(" ", "-").lower()
                            category_2 = climate_generic_category.replace(" ", "").lower()
                    submenu_key = category or category_1 or category_2 or submenu_key

                if submenu_key == 'agriculture':
                    submenu_key = 'food'
                elif submenu_key == 'businessusa':
                    submenu_key = 'business'
                elif submenu_key == 'County Government':
                    submenu_key = 'counties'
                elif submenu_key == 'State Government':
                    submenu_key = 'states'
                elif submenu_key == 'City Government':
                    submenu_key = 'cities'
                elif submenu_key == 'hhs-gov':
                    submenu_key = 'health'

    if submenu_key:
        navigations = None
        if category_1 or category_2:
            navigations = menus.get(category_1 + '_navigation', menus.get(category_2 + '_navigation'))
        else:
            navigations = menus.get(submenu_key + '_navigation')


        if navigations:
            submenus = []
            for submenu in navigations:
                if re.search(r'/#$', submenu['link']):
                    submenu['has_children'] = True
                submenus.append(submenu)
            menus['submenus'] = submenus

            name_pair = {
            'jobs-and-skills': 'Jobs & Skills',
            'development': 'Global Development',
            'research': 'Science & Research',
            'food': 'Agriculture',
            'coastalflooding': ['Climate', 'Coastal Flooding'],
            'foodresilience': ['Climate', 'Food Resilience'],
            }
            if climate_generic_category:
                if category_1:
                    name_pair[category_1] = ['Climate', climate_generic_category]
                if category_2:
                    name_pair[category_2] = ['Climate', climate_generic_category]

            parent = {}
            name = name_pair.get(submenu_key, submenu_key.capitalize())
            if type(name) is list:
                parent['key'] = name[0].lower() # hope nothing breaks here
                parent['url'] = '//www.data.gov/' + parent['key']
                parent['class'] = 'topic-' + parent['key']

            menus['topic_header'] = {
                'multi': True if parent else False,
                'url': '//www.data.gov/' + submenu_key if not parent else [parent['url'], '//www.data.gov/' + submenu_key],
                'name': name,
                'class': 'topic-' + submenu_key if not parent else parent['class'],
            }

    return menus

def get_collection_package(collection_package_id):
    package = p.toolkit.get_action('package_show')({}, {'id': collection_package_id})
    return package