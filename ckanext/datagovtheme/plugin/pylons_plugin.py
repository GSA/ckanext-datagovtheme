"""
Mixin for Pylons-specific functionality. This aides the migration between Pylons and Flask.
"""
import ckan.plugins as p


class MixinPlugin(object):

    # IConfigurer
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        p.toolkit.add_template_directory(config, '../templates/templates_2_8')
        p.toolkit.add_public_directory(config, '../public')
        p.toolkit.add_resource('../fanstatic_library_2_8', 'datagovtheme')
