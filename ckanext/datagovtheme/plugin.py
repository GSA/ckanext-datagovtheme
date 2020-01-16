import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from sqlalchemy.util import OrderedDict

class DatagovTheme(p.SingletonPlugin):
    '''An example theme plugin.

    '''
    # Declare that this class implements IConfigurer.
    p.implements(p.IConfigurer)
    p.implements(p.IFacets, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_resource('fanstatic_library', 'datagovtheme')
    
    ## IFacets
    def dataset_facets(self, facets_dict, package_type):

        if package_type != 'dataset':
            return facets_dict

        return OrderedDict([('groups', 'Topics'),
                            ('vocab_category_all', 'Topic Categories'),
                            ('metadata_type','Dataset Type'),
                            ('tags','Tags'),
                            ('res_format', 'Formats'),
                            ('organization_type', 'Organization Types'),
                            ('organization', 'Organizations'),
                            ('publisher', 'Publishers'),
                            ('bureauCode', 'Bureaus'),
                           ## ('extras_progress', 'Progress'),
                           ])

    def organization_facets(self, facets_dict, organization_type, package_type):

        if not package_type:
            return OrderedDict([('groups', 'Topics'),
                                ('vocab_category_all', 'Topic Categories'),
                                ('metadata_type','Dataset Type'),
                                ('tags','Tags'),
                                ('res_format', 'Formats'),
                                ('groups', 'Topics'),
                                ('harvest_source_title', 'Harvest Source'),
                                ('capacity', 'Visibility'),
                                ('dataset_type', 'Resource Type'),
                                ('publisher', 'Publishers'),
                                ('bureauCode', 'Bureaus'),
                               ])
        else:
            return facets_dict
    
    def group_facets(self, facets_dict, organization_type, package_type):

        # get the categories key
        group_id = p.toolkit.c.group_dict['id']
        key = 'vocab___category_tag_%s' % group_id
        if not package_type:
            return OrderedDict([(key, 'Categories'),
                                ('metadata_type','Dataset Type'),
                                ('organization_type', 'Organization Types'),
                                ('tags','Tags'),
                                ('res_format', 'Formats'),
                                ('organization', 'Organizations'),
                                (key, 'Categories'),
                                #('publisher', 'Publisher'),
                               ])
        else:
            return facets_dict
        
    ## IRoutes
    def before_map(self, map):
        controller = 'ckanext.datagovtheme.controllers:ViewController'
        map.connect('map_viewer', '/viewer',controller=controller, action='show')
        map.redirect('/', '/dataset')
        return map

    ## ITemplateHelpers
    def get_helpers(self):
        from ckanext.datagovtheme import helpers as datagovtheme_helpers
        return {
            'render_datetime_datagov': datagovtheme_helpers.render_datetime_datagov,
            'get_harvest_object_formats': datagovtheme_helpers.get_harvest_object_formats,
            'get_dynamic_menu': datagovtheme_helpers.get_dynamic_menu,
            'get_bureau_info': datagovtheme_helpers.get_bureau_info,
            'get_harvest_source_link': datagovtheme_helpers.get_harvest_source_link,
            'is_web_format': datagovtheme_helpers.is_web_format,
            'is_map_viewer_format' : datagovtheme_helpers.is_map_viewer_format,
            'get_map_viewer_params': datagovtheme_helpers.get_map_viewer_params,
            'resource_preview_custom': datagovtheme_helpers.resource_preview_custom,
            'is_preview_format': datagovtheme_helpers.is_preview_format,
            'is_map_format': datagovtheme_helpers.is_map_format,
            'is_plotly_format': datagovtheme_helpers.is_plotly_format,
            'is_cartodb_format': datagovtheme_helpers.is_cartodb_format,
            'is_arcgis_format': datagovtheme_helpers.is_arcgis_format,
            'arcgis_format_query': datagovtheme_helpers.arcgis_format_query,
            'convert_resource_format':datagovtheme_helpers.convert_resource_format,
            'remove_extra_chars':datagovtheme_helpers.remove_extra_chars,
            'schema11_key_mod':datagovtheme_helpers.schema11_key_mod,
            'schema11_frequency_mod':datagovtheme_helpers.schema11_frequency_mod,
            'convert_top_category_to_list':datagovtheme_helpers.convert_top_category_to_list,
            'is_bootstrap2':datagovtheme_helpers.is_bootstrap2,
        }
