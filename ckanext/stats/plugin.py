from logging import getLogger

import ckan.plugins as p

import ckan.model as model

def dts_id_to_name(id):
    return model.Session.query(model.Package).filter(model.Package.id == id).first().title

log = getLogger(__name__)

class StatsPlugin(p.SingletonPlugin):
    '''Stats plugin.'''

    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=False)

    def after_map(self, map):
        map.connect('stats', '/stats',
            controller='ckanext.stats.controller:StatsController',
            action='index')
        map.connect('stats_action', '/stats/{action}',
            controller='ckanext.stats.controller:StatsController')
        return map

    def update_config(self, config):
        templates = 'templates'
        if p.toolkit.asbool(config.get('ckan.legacy_templates', False)):
                templates = 'templates_legacy'
        p.toolkit.add_template_directory(config, templates)
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_resource('public/ckanext/stats', 'ckanext_stats')

    def get_helpers(self):
        return {'dts_id_to_name': dts_id_to_name }
