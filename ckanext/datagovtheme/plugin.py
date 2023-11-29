import ckan.plugins as p
from sqlalchemy.util import OrderedDict

p.toolkit.requires_ckan_version("2.9")

from . import blueprint


class DatagovTheme(p.SingletonPlugin):
    '''Theme plugin for catalog.data.gov.'''

    # Declare the iterfaces this class implements
    p.implements(p.IBlueprint)
    p.implements(p.IConfigurer)
    p.implements(p.IFacets, inherit=True)
    p.implements(p.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_resource('fanstatic_library', 'datagovtheme')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):

        if package_type != 'dataset':
            return facets_dict

        return OrderedDict([('groups', 'Topics'),
                            ('vocab_category_all', 'Topic Categories'),
                            ('metadata_type', 'Dataset Type'),
                            ('tags', 'Tags'),
                            ('res_format', 'Formats'),
                            ('organization_type', 'Organization Types'),
                            ('organization', 'Organizations'),
                            ('publisher', 'Publishers'),
                            ('bureauCode', 'Bureaus'),
                            # ('extras_progress', 'Progress'),
                            ])

    def organization_facets(self, facets_dict, organization_type, package_type):

        if not package_type:
            return OrderedDict([('groups', 'Topics'),
                                ('vocab_category_all', 'Topic Categories'),
                                ('metadata_type', 'Dataset Type'),
                                ('tags', 'Tags'),
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

        # For https://github.com/GSA/datagov-deploy/issues/3630
        # re-evaluate necessity of these two lines after ckan 2.9.6.
        if organization_type == 'organization':
            return self.organization_facets(facets_dict, organization_type, package_type)

        # get the categories key
        group_id = p.toolkit.c.group_dict['id']
        key = 'vocab___category_tag_%s' % group_id
        if not package_type:
            return OrderedDict([(key, 'Categories'),
                                ('metadata_type', 'Dataset Type'),
                                ('organization_type', 'Organization Types'),
                                ('tags', 'Tags'),
                                ('res_format', 'Formats'),
                                ('organization', 'Organizations'),
                                (key, 'Categories'),
                                # ('publisher', 'Publisher'),
                                ])
        else:
            return facets_dict

    # ITemplateHelpers
    def get_helpers(self):
        from ckanext.datagovtheme import helpers as datagovtheme_helpers
        # TODO prefix these helper names with datagovtheme_
        helpers = {
            'datagovtheme_api_doc_url': datagovtheme_helpers.api_doc_url,
            'datagovtheme_get_reference_date': datagovtheme_helpers.get_reference_date,
            'datagovtheme_get_responsible_party': datagovtheme_helpers.get_responsible_party,
            'is_tagged_ngda': datagovtheme_helpers.is_tagged_ngda,
            'render_datetime_datagov': datagovtheme_helpers.render_datetime_datagov,
            'get_harvest_object_formats': datagovtheme_helpers.get_harvest_object_formats,
            'get_bureau_info': datagovtheme_helpers.get_bureau_info,
            'get_harvest_source_link': datagovtheme_helpers.get_harvest_source_link,
            'is_web_format': datagovtheme_helpers.is_web_format,
            'is_map_viewer_format': datagovtheme_helpers.is_map_viewer_format,
            'get_map_viewer_params': datagovtheme_helpers.get_map_viewer_params,
            'is_preview_format': datagovtheme_helpers.is_preview_format,
            'is_map_format': datagovtheme_helpers.is_map_format,
            'is_plotly_format': datagovtheme_helpers.is_plotly_format,
            'is_cartodb_format': datagovtheme_helpers.is_cartodb_format,
            'is_arcgis_format': datagovtheme_helpers.is_arcgis_format,
            'arcgis_format_query': datagovtheme_helpers.arcgis_format_query,
            'convert_resource_format': datagovtheme_helpers.convert_resource_format,
            'remove_extra_chars': datagovtheme_helpers.remove_extra_chars,
            'schema11_key_mod': datagovtheme_helpers.schema11_key_mod,
            'schema11_frequency_mod': datagovtheme_helpers.schema11_frequency_mod,
            'convert_top_category_to_list': datagovtheme_helpers.convert_top_category_to_list,
            'get_pkg_dict_extra': datagovtheme_helpers.get_pkg_dict_extra,
            'get_login_url': datagovtheme_helpers.get_login_url,
        }

        # https://github.com/GSA/ckan/blob/datagov/ckan/config/environment.py#L70:L70
        # Override ckanext-qa and ckanext-archiver template helpers. Is this best practice?
        override_helpers = {
            'archiver_resource_info_table': datagovtheme_helpers.archiver_resource_info_table,
            'archiver_is_resource_broken_line': datagovtheme_helpers.archiver_is_resource_broken_line,
            'qa_openness_stars_resource_line': datagovtheme_helpers.qa_openness_stars_resource_line,
            'qa_openness_stars_resource_table': datagovtheme_helpers.qa_openness_stars_resource_table,
        }

        helpers.update(override_helpers)

        return helpers

    def get_blueprint(self):
        return blueprint.pusher
