import ckan.plugins as p


def test_helpers_collition():
    """ To fix helpers name collition in CKAN 2.3
        https://github.com/GSA/ckanext-datagovtheme/pull/53
    """

    if not p.toolkit.check_ckan_version(max_version='2.3'):
        return

    extra_helpers = []
    for plugin in p.PluginImplementations(p.ITemplateHelpers):
        helpers = plugin.get_helpers()
        for helper in helpers:
            if helper in extra_helpers:
                raise Exception('overwritting extra helper %s' % helper)
            extra_helpers.append(helper)
